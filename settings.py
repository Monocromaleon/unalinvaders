from pygame import event

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
PLAY_MUSIC = True


CUSTOM_EVENTS = {
    'ADD_PLAYER_BULLET': event.custom_type(),
    'ADD_ALIEN': event.custom_type(),
    'ADD_ALIEN_BULLET': event.custom_type(),
    'ADD_BONUS': event.custom_type(),
    'ADD_BONUS_BULLET': event.custom_type()
}
