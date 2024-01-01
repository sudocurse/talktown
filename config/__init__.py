from config.appearance_config import AppearanceConfig
from config.artifact_config import ArtifactConfig
from config.basic_config import BasicConfig
from config.businesses_config import BusinessesConfig
from config.life_cycle_config import LifeCycleConfig
from config.marriage_config import MarriageConfig
from config.misc_character_config import MiscellaneousCharacterConfig
from config.misc_decision_making_config import MiscellaneousCharacterDecisionMakingConfig
from config.personality_config import PersonalityConfig
from config.routine_config import RoutineConfig
from config.salience_config import SalienceConfig
from config.social_sim_config import SocialSimConfig
from config.story_recognition_config import StoryRecognitionConfig
from config.town_generation_details_config import TownGenerationDetailsConfig

ALL_CONFIG_FILES = [
    AppearanceConfig, ArtifactConfig, BasicConfig, BusinessesConfig, LifeCycleConfig, MarriageConfig,
    MiscellaneousCharacterConfig, MiscellaneousCharacterDecisionMakingConfig, PersonalityConfig,
    RoutineConfig, SalienceConfig, SocialSimConfig, StoryRecognitionConfig, TownGenerationDetailsConfig
]


class Config(object):
    """A class that aggregates all author-defined configuration parameters."""

    def __init__(self):
        """Initialize a Config object."""
        # This short script will slurp up all the parameters included in the various configuration
        # files -- specified as attributes on the classes defined in those files -- and set those
        # as attributes on the Config class defined above; this class will then be set as an attribute
        # on the Simulation object constructed by Simulation.__init__(), which will make all of the
        # config parameters accessible through 'Simulation.config'
        for config_file in ALL_CONFIG_FILES:
            for parameter, value in list(config_file.__dict__.items()):
                self.__dict__[parameter] = value
