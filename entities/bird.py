import pygame

class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.imgs = imgs
        self.actual_img = imgs[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL   

    def draw(self, screen):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.actual_img = self.imgs[0]

        elif self.img_count < self.ANIMATION_TIME*2:
            self.actual_img = self.imgs[1]

        elif self.img_count < self.ANIMATION_TIME*3:
            self.actual_img = self.imgs[2]

        elif self.img_count < self.ANIMATION_TIME*4:
            self.actual_img = self.imgs[1]

        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.actual_img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.actual_img = self.imgs[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.actual_img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.actual_img.get_rect(topleft = (self.x, self.y)).center)

        screen.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.actual_img)

