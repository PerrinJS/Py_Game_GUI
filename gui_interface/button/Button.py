import pygame

class Button:
    '''
    This is a class for drawing buttons in pygame.
    It reqires pygame to already be initialized and a screen to be given.
    '''

    _BACKGROUND_COLOR = 255, 255, 255
    _HIGHLIGHT_COLOR  =   0,   0,   0
    _HIGHLIGHT_WIDTH  = 1

    clicked_before = False

    #TODO: make the width and height optional such that when it's not included
    #    we use the width of the text to bind it
    #TODO: implement a full suite of getters and setters
    def __init__(self, display: pygame.Surface, width=None, height=None,
                 x=0, y=0, text=None, command=None):
        #TODO: Figure out if there is a better solution
        if isinstance(display, pygame.Surface):
            self.parent: pygame.Surface = display
        else:
            raise TypeError("display must be of type pygame.Surface")

        #So we don't need to worry about conversion later
        if width != None and height != None:
            self.width = int(width)
            self.height = int(height)
        else:
            #TODO: set the width and height based on the bounding box
            pass

        self.x = int(x)
        self.y = int(y)

        #TODO: make this modifiable
        self.bgColor = self._BACKGROUND_COLOR
        self.fgColor = self._HIGHLIGHT_COLOR

        #TODO: find a better way to check the type of this
        if (command is not None) and (isinstance(command, type(lambda: 0))):
            self.command = command
        elif command is not None:
            #TODO: throw and error
            pass
        else:
            self.command = None

        # #This way were not storing a large object just what we will put int the
        # #string
        # self.text = str(text)
        #Make the text object
        #TODO: when the text object is changed we need to remake this
        #TODO: allow setting the font type and size
        text_font = pygame.font.SysFont(pygame.font.get_default_font(), 12)
        self.text = text_font.render(str(text), False, self._HIGHLIGHT_COLOR)
        #Centers the text over the button initializeing self.text_rect
        self._recenter_text()

    #### HELPERS ####

    def _recenter_text(self):
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self._get_button_center()

    def _get_button_center(self):
        return (self.x + (self.width // 2), self.y + (self.height // 2))

    def _get_parent_size(self):
        return self.parent.get_size()

    def _is_mouse_in_range(self):
        ret = False
        mousePos = pygame.mouse.get_pos()
        tmpSize = self.width, self.height

        #is the current mouse position within the button area
        inXArea = self.x <= mousePos[0] <= (self.x + tmpSize[0])
        inYArea = self.y <= mousePos[1] <= (self.y + tmpSize[1])
        if inXArea and inYArea:
            ret = True

        return ret

    def _is_tuple_of_len(self, value, length):
        return (isinstance(value, tuple) and (len(value) == length))

    def _color_setter_type_ok(self, color):
        macrotype_ok = self._is_tuple_of_len(color, 3)
        valuetype_ok = (isinstance(color[0], int) and
                        isinstance(color[1], int) and
                        isinstance(color[2], int))
        return macrotype_ok and valuetype_ok

    def _pos_setter_type_ok(self, pos):
        macrotype_ok = self._is_tuple_of_len(pos, 2)
        #TODO: figure a better way of doing this
        #valuetype_ok = (int == type(pos[0]) == type(pos[1]))
        #return macrotype_ok and valuetype_ok
        return macrotype_ok

    def _draw_hover_highlight(self):
        #So we get a nice border around the highlight rect
        rectPosNSize = pygame.Rect(
                self.x + 1,
                self.y + 1,
                self.width - 1 - self._HIGHLIGHT_WIDTH,
                self.height - 1 - self._HIGHLIGHT_WIDTH)

        pygame.draw.rect(self.parent, self.fgColor, rectPosNSize,
                self._HIGHLIGHT_WIDTH)

    def _clicked(self):
        button_down = self._button_down()
        ret = False
        if button_down:
            #Stop repeats
            if not self.clicked_before:
                ret = True
                self.clicked_before = True
        else:
            self.clicked_before = False
        return ret

    def _button_down(self):
        ret = False
        if self._is_mouse_in_range():
            if pygame.mouse.get_pressed()[0]:
                ret = True
        return ret

    #### GETTERS ####

    def get_fg_color(self):
        return self.fgColor

    def get_bg_color(self):
        return self.bgColor

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    #### SETTERS ####
    #TODO: Go through all thease and make sure that the pos of the text is being set correctly

    def draw(self):
        clicked = self._clicked()
        button_down = self._button_down()
        hovering = self._is_mouse_in_range()

        pygame.draw.rect(
                self.parent,
                self.bgColor,
                (self.x, self.y, self.width, self.height))

        #TODO: blit in the text here
        self.parent.blit(self.text, self.text_rect)

        #if we clicked then we do nothing thus using the origenal appearence
        if hovering and not button_down:
            self._draw_hover_highlight()
        elif (self.command is not None) and clicked:
            self.command()

    def set_fg_color(self, color):
        if self._color_setter_type_ok(color):
            self.fgColor = color
        else:
            raise TypeError("Color values should be a three integer tuple")

    def set_bg_color(self, color):
        if self._color_setter_type_ok(color):
            self.bgColor = color
        else:
            raise TypeError("Color values should be a three integer tuple")

    def set_pos(self, pos):
        if self._pos_setter_type_ok(pos):
            self.x = int(pos[0])
            self.y = int(pos[1])
            # Update the text position relative to the new x and y positions
            self._recenter_text()
