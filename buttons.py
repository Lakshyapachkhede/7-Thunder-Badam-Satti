import pygame
pygame.init()
pygame.mixer.init()

font_button = pygame.font.Font(r"assets\fonts\Boniro.ttf", 30)
clickSound = pygame.mixer.Sound(r"assets\sound\click.mp3")


class Button:
    def __init__(self, x, y, width, height, color, hover_color, border_color, text_color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_color = text_color
        self.text = text
        self.action = action

    def draw(self, surface):
        # Draw background
        if self.is_mouse_over():
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=10)

        # Draw text
        text_surface = font_button.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)

    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)

    def activate_button(self, window):
        self.draw(window)
        if self.is_mouse_over() and pygame.mouse.get_pressed()[0]:
            clickSound.play()
            if self.action != None:
                self.action()
            return True


if __name__ == "__main__":
    pass