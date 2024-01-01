import sys
import time
from simulation import Simulation
import os
import threading

# Generate a town!
start_time = time.time()
sim = Simulation()  # Objects of the class Simulation are Talk of the Town simulations
# Simulate from the date specified as the start of town generation to the date specified
# as its terminus; both of these dates can be set in config/basic_config.py
name = '{:X}'.format(hash(time.time()))
sys.stdout.write(name+"\n")
sys.stdout.flush()

try:
    if not os.path.exists(name):
        os.makedirs(name)
        os.makedirs(name+'/characters')
    with open('{}/worldgen.txt'.format(name), 'w') as logger:
        sim.establish_setting(logger)  # This is the worldgen procedure; it will simulate until the date specified in basic_config.py
        town = sim.town
except KeyboardInterrupt:  # Enter "ctrl+C" (a keyboard interrupt) to end worldgen early
    # In the case of keyboard interrupt, we need to tie up a few loose ends
    # sys.stdout.write('\r{}'.format(' ' * 94))  # Clear out the last sampled event written to stdout
    # sys.stdout.write('\rWrapping up...')
    sim.advance_time()
    for person in list(sim.town.residents):
        person.routine.enact()
# Town generation was successful, so print out some basic info about the town
with open('{}/summary.md'.format(name), 'w') as logger:
    logger.write("\nAfter {time_elapsed}s, town generation was successful!".format(
        time_elapsed=int(time.time()-start_time)) + "\n")
    # Print out the town, population, and date
    logger.write("\nIt is now the {date}, in the town of {town}, pop. {population}.\n".format(
        date=sim.date[0].lower() + sim.date[1:],
        town=sim.town.name,
        population=sim.town.population)  + "\n")
    # Start excavating nuggets of dramatic intrigue from the raw emergent material produced
    # during the simulation of the town's history
    logger.write("Excavating nuggets of dramatic intrigue..." + "\n")
    sim.story_recognizer.excavate(logger)


# Save all this material to global variables, for convenience
unrequited_love_cases = sim.story_recognizer.unrequited_love_cases
love_triangles = sim.story_recognizer.love_triangles
extramarital_romantic_interests = sim.story_recognizer.extramarital_romantic_interests
asymmetric_friendships = sim.story_recognizer.asymmetric_friendships
misanthropes = sim.story_recognizer.misanthropes
sibling_rivalries = sim.story_recognizer.sibling_rivalries
business_owner_rivalries = sim.story_recognizer.business_owner_rivalries

# To simulate ahead in time, simply use the 'Simulation.simulate()' method (given
# that we binded a Simulation object to the variable 'sim' above, you can call this
# using sim.simulate()'), which takes the number of timesteps as its argument. There's 
# two timesteps for each day (one for daytime, one for nighttime), so Simulation.simulate(730) 
# will simulate one year, and so forth.

# To retrieve a person (i.e., the Python object in memory that represents them) by
# their name, use the command Simulation.find_person(string_of_their_full_name), e.g.,
# Simulation.find('James Ryan').

# Here's some other quick commands that you can use to explore your generated town.

def outline_businesses(logger=sys.stdout):
    """Outline all the businesses, past and present, in this town."""
    logger.write( '\nFormer businesses in {town}:\n\n'.format(town=sim.town.name))
    for c in sim.town.former_companies:
        logger.write('\t{}\n\n'.format(c))
    logger.write('\nCurrent businesses in {town}:\n\n'.format(town=sim.town.name))
    for c in sim.town.companies:
        logger.write('\t{}\n\n'.format(c))


def outline_character_locations(logger=sys.stdout):
    """Outline the locations in town, and who is currently at each one."""
    for location in sim.town.companies|sim.town.dwelling_places:
        logger.write("## " + str(location) + "\n\n")
        if not location.people_here_now:
            logger.write('\tno one here' + "\n")
        else:
            try:
                for character in location.people_here_now:
                    if character.routine.working:
                        logger.write("\t{} (working as {})".format(character, character.routine.occasion, character.occupation.vocation) + "\n")
                    else:
                        logger.write("\t{} ({})".format(character, character.routine.occasion) + "\n")
            finally:
                pass

def outline_gravestones(logger=sys.stdout):
    """Print out all the gravestones in the town."""
    for d in sim.town.deceased:
        logger.write("```{}```".format(str(d.gravestone.description) + "\n"))


def outline_character_social_network(person, logger=sys.stdout):
    """Print out a character's relationships to everyone else in the town."""
    for resident in sim.town.residents:
        logger.write(str(person.relation_to_me(resident)) + "\n")


def outline_relationship(person, other_person, logger=sys.stdout):
    """Outline the unidirectional relationships between these two."""
    if other_person not in person.relationships:
        # logger.write(None)
        pass
    else:
        logger.write("\t{}'s relationship toward {}:".format(person, other_person) + "\n")
        logger.write(person.relationships[other_person].outline() + "\n")
        logger.write('\n')
        logger.write("\t{}'s relationship toward {}:".format(other_person, person) + "\n")
        logger.write(other_person.relationships[person].outline() + "\n")


def list_attributes(entity, logger=sys.stdout):
    """Print out a list of attributes that an entity has.

    This will specifically print out a list of attributes that the object passed for
    the 'entity' argument has. You can then see what values are held in these attributes by
    using simple dot-notation commands. For instance, if a person has the attribute 'neighbors',
    you can see what's held in that attribute by using a command like 'print entity.neighbors'.

    The listing of attributes won't give an exhuastive account of the kinds of data that are
    stored for most entities, since some attributes will hold objects that themselves have
    attributes. For example, 'person.face' will hold a Face object, which itself will have
    attributes holding objects pertaining to components of the face. Generally, though, the
    listing	produced by this function should give you a good idea of some of the kinds of data
    that are stored (some of which may be narratively potent).

    Additionally, any attributes that are computed dynamically (by using Python @property
    decorators) won't show up. Here's a current list of those kinds of attributes for Person
    objects:
        age_and_gender_description
        basic_appearance_description
        boss
        dead
        description
        first_home
        full_name
        full_name_without_suffix
        honorific
        is_captivated_by
        kids_at_home
        life_events
        name
        nametag
        next_of_kin
        nuclear_family
        object_pronoun
        possessive_pronoun
        present
        queer
        reflexive_pronoun
        requited_love_interest
        subject_pronoun
        year_i_moved_here
        years_i_lived_here
    """
    for attribute in sorted(vars(entity).keys()):  # Prints them out in alphabetical order
        logger.write(str(attribute) + "\n")


def outline_physical_description(person, logger=sys.stdout):
    """Outline a person's physical description."""
    logger.write(str(person.description) + "\n")


def outline_personality(person, logger=sys.stdout):
    """Outline a person's physical description."""
    str = "\nFive-factor personality model of {}:\n\n".format(person.name)
    str += "\tOpenness: {}{}\n".format(
        person.personality.component_str('o'),
        '' if not person.personality.o.inherited_from else
        ' (takes after {})'.format(person.personality.o.inherited_from.name)
    )
    str += "\tConscientiousness: {}{}\n".format(
        person.personality.component_str('c'),
        '' if not person.personality.c.inherited_from else
        ' (takes after {})'.format(person.personality.c.inherited_from.name)
    )
    str += "\tExtroversion: {}{}\n".format(
        person.personality.component_str('e'),
        '' if not person.personality.e.inherited_from else
        ' (takes after {})'.format(person.personality.e.inherited_from.name)
    )
    str += "\tAgreeableness: {}{}\n".format(
        person.personality.component_str('a'),
        '' if not person.personality.a.inherited_from else
        ' (takes after {})'.format(person.personality.a.inherited_from.name)
    )
    str += "\tNeuroticism: {}{}\n".format(
        person.personality.component_str('n'),
        '' if not person.personality.n.inherited_from else
        ' (takes after {})'.format(person.personality.n.inherited_from.name)
    )
    logger.write(str + "\n")


def outline_love_life(person, logger=sys.stdout):
    """Outline a person's love life, including their strongest love interest and anyone else they are
    very interested in romantically.
    """
    spouse = person.spouse
    other_love_interests = sorted(person.is_captivated_by, key=lambda li: person.relationships[li].spark, reverse=True)
    if spouse in other_love_interests:
        other_love_interests.remove(spouse)
    str = "\nRomantic life of {}:\n\n".format(person.name)
    if person.spouse:
        str += "\tSpouse: {name} ({person_spark_for_them} {heart_emoji} {their_spark_for_person})\n".format(
            name=spouse.name,
            person_spark_for_them=person.relationships[person.spouse].spark,
            heart_emoji='\xe2\x9d\xa4',
            their_spark_for_person=person.spouse.relationships[person].spark
        )
    else:
        str += "\tSpouse: none\n"
    if other_love_interests:
        str += "\tOther love interests: {}\n".format(
            ', '.join('{name} ({person_spark_for_them} {heart_emoji} {their_spark_for_person})'.format(
                name=other_love_interest.name,
                person_spark_for_them=person.relationships[other_love_interest].spark,
                heart_emoji='\xe2\x9d\xa4',
                their_spark_for_person=other_love_interest.relationships[person].spark
            ) for other_love_interest in other_love_interests)
        )
    else:
        str += "\tOther love interests: none\n"
    logger.write(str + "\n")


def outline_family(person, logger=sys.stdout):
    """Outline a person's family members."""
    str = "\n".join(["\nFamily of {}:\n".format(person.name),
        "\tSpouse: {}\n".format(person.spouse.name if person.spouse else 'none'),
        "\tChildren: {}\n".format(', '.join(x.name for x in person.kids) if person.kids else 'none'),
        "\tGrandchildren: {}\n".format(', '.join(x.name for x in person.grandchildren) if person.grandchildren else 'none'),
        "\tGrandchildren: {}\n".format(', '.join(x.name for x in person.greatgrandchildren) if person.greatgrandchildren else 'none'),
        "\tParents: {}\n".format(', '.join(x.name for x in person.parents) if person.parents else 'none'),
        "\tBrothers: {}\n".format(', '.join(x.name for x in person.brothers) if person.brothers else 'none'),
        "\tSisters: {}\n".format(', '.join(x.name for x in person.sisters) if person.sisters else 'none'),
        "\tGrandparents: {}\n".format(', '.join(x.name for x in person.grandparents) if person.grandparents else 'none'),
        "\tGreatgrandparents: {}\n".format(', '.join(x.name for x in person.greatgrandparents) if person.greatgrandparents else 'none'),
        "\tAunts: {}\n".format(', '.join(x.name for x in person.aunts) if person.aunts else 'none'),
        "\tUncles: {}\n".format(', '.join(x.name for x in person.uncles) if person.uncles else 'none'),
        "\tNieces: {}\n".format(', '.join(x.name for x in person.nieces) if person.nieces else 'none'),
        "\tNephews: {}\n".format(', '.join(x.name for x in person.nephews) if person.nephews else 'none'),
         "\tCousins: {}\n".format(', '.join(x.name for x in person.cousins) if person.cousins else 'none')])
    logger.write( str + "\n")


def list_ancestors(person, logger=sys.stdout):
    """List all of a person's ancestors."""
    for ancestor in person.ancestors:
            logger.write( str(ancestor) + "\n\n")


def list_work_history(person, logger=sys.stdout):
    """List out a person's occupational history."""
    for o in person.occupations:
            logger.write( str(o) + "\n\n")

def write_character(p):

    with open("{}/characters/{}.md".format(name, p.__repr__().replace(" ", "-")), 'w') as f:
        f.write("# {}\n".format(str(p)))
        outline_physical_description(p, logger=f)
        logger.write("## Personality\n\n")
        outline_personality(p, logger=f)
        logger.write("## Romantic Life\n\n")
        outline_love_life(p, logger=f)
        logger.write("## All Relationships\n\n")
        for resident in sim.town.residents:
            if p.relation_to_me(resident):
                f.write("{}: {}\n\n".format(str(resident), str(p.relation_to_me(resident))))
        logger.write("## Work History\n\n")
        list_work_history(p, logger=f)
        logger.write("## Family\n\n")
        outline_family(p, logger=f)
        logger.write("## Ancestors\n\n")
        list_ancestors(p, logger=f)

def print_em_all():

    threads = []
    characters = {}

    def a():
        with open("{}/locations.md".format(name), 'w') as f:
            outline_character_locations(logger=f)

    threads.append(threading.Thread(target=a))

    for p in list(sim.town.residents):
        canonical_person_name = p.__repr__().replace(" ", "-")
        characters[canonical_person_name] = str(p)
        # threads.append(threading.Thread(target=write_character,args=([p])))
        write_character(p)


    # print "# Landmarks"

    # print "## Businesses"
    def b():
        with open("{}/landmark.md".format(name), 'w') as f:
            outline_businesses(logger=f)
            # print "## Gravestones"
            outline_gravestones(logger=f)
            # print "# Stories"

    threads.append(threading.Thread(target=b))

    stuff = [ unrequited_love_cases,
              love_triangles,
              extramarital_romantic_interests,
              asymmetric_friendships,
              misanthropes,
              sibling_rivalries,
              business_owner_rivalries ]

    def c():
        with open("{}/drama.md".format(name), 'a') as f:
            for category in stuff:
                for x in category:
                    f.write(x + "\n\n")

    threads.append(threading.Thread(target=c))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    char_toc = ""
    for x in characters:
        char_toc += "    - [{}](characters/{}.md)\n".format(characters[x], x)
    toc = """
- [Summary](summary.md)
- [Locations](locations.md)
- [Businesses & gravestones](landmark.md)
- [Tea](drama.md)
- Characters

""" + char_toc
    with open("{}/README.md".format(name), 'w') as f:
        f.write(toc)



print_em_all()