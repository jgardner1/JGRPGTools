The JGRPG Rule System
=====================

This section covers the JGRPG Rule System.

========
Overview
========

We're going to first cover what types of objects exist within the system, and
then we'll cover how those objects interact with each other.

=============
Basic Objects 
=============

The Rule System relies on only a few types of objects. These are listed below.

-------------------
Objects and Prototypes
-------------------

If you've used Javascript before, this system of objects and prototypes will
sound familiar. If you haven't, that's ok. I'm going to explain it here.

An *object* is something that has a set of *attributes* associated with it.
These attributes could be things like Hit Points or Strength, or things like
the number of spells memorized but not yet cast for Characters. For Items, it
would be the item name and type, its weight and its value.

In terms of how objects behave, the attributes are all that matter. Modify the
attributes to modify its behavior.

A *prototype* is a special object that is used to create other objects. When
you create an object from a prototype, the object refers back to the prototype
for its attributes. We call the object and *instance* of the prototype when it
is created in that way. The prototype may also contain instructions on how to
create objects from it.

The attributes of an object are either authoritative or calculated.
Authoritative attributes are attributes that are inherent in the object and
cannot be changed. This would be things like base Strength and Intelligence.
There is nothing you can do to change a character's basic attributes. If you
want more Strength or Intelligence, you have to apply *effects* to the
creature to give it that. Calculated attributes are calculated from
authoritative attributes and effects. For instance, the actual Strength of a
character would be the sum of its inherent Strength and whatever effects it
had due to strength potions, skills, traits, etc...

-------------------
Players and GM
-------------------

Although these are not objects like the others in that they exist outside the
imagined universe of the RPG, they are nonetheless objects. There are classes
in the code that represent them.

A *Player* is someone who is playing the game. Typically, a player controls a
single character. (When you are short players, you can have a player play several
characters.)

The *Game Master* (GM) is the equivalent of the Dungeon Master in Dungeons and
Dragons. The Game Master is responsible for the entire game and its execution.

When using the JGRPG Toolkit, the GM generally has greater access to the
internals of the game than the Players do. The GM hosts the entire game and is
free to manipulate any aspect of the universe he desires, going so far as
being able to change the results of actions if he wants to. The reason for
this is simple: The GM is really a story-teller. The players are story-tellers
as well, of course, telling the story of their characters, but the GM has to
tell the story of everything else.

--------------------
Characters and Races
--------------------

*Characters* are the intelligent beings that inhabit the universe. They are
instances of the *Race* objects, which are really character prototypes.

Characters can be *player characters* (PCs) or *non-player characters* (NPCs).
Either way, someone has to tell them what to do. In the case of PCs, the
players choose what those characters will do. In the case of NPCs, either the
GM or the system determines their actions.

The attributes of the characters and races and their meanings are not listed
here. You can find them in the code documentation for Race and Character.

-------------------------
Items and Item Prototypes
-------------------------

An *Item* is the object that characters can pick up and interact with. They
have attributes as well as any other object, of course. Some items are
weapons, others are armor, and still others are trinkets and various devices
that may or may not have magical effects.

Items are largely passive. They tend not to do things on their own. They
establish an Effect and that is pretty much it. However, some items are
intelligent and can be interacted with in more ways than simply "using" it.

*Item Prototypes* are general classes of items. Shortsword, for instance, is
an Item Prototype. The Shortsword that Sir Gallahad is carrying is not a
prototype, but an instance of the prototype.


------------------------
Areas and Area Prototypes
------------------------

*Areas* cover all locations, whether the entire universe or just a room in a
dungeon. Area can be nested in other areas. Areas are the device through which
items and characters see each other and interact with each other. Physical
closeness is represented by being in similar areas.

The basic JGRPG Toolkit does not provide an XY coordinate for characters in an
Area. Rather, it is like the old-school text adventures of MUDs. Being in a
room means you are somewhere in that room. It is not defined where exactly,
because knowing that the character or item is in the Area is enough
information.

*Area Prototypes* are used to generate new Areas. There are a variety of
prototypes available, and you can make your own.

------------------------
Groups and Hordes
------------------------

A *Group* is a set of individual characters. They have a specific number. Item
ownership may be transferred to the group. Or rather, the group can claim
ownership of things, even though someone in the group is carrying it. A Group
can be a party of adventurers, a small patrol of goblin marauders, or a dragon
by itself.

What's important to note is that groups battle each other. Individual
characters cannot. Think of the old-style Bard's Tale, and you will have a
good idea of how combat proceeds. The exact position of the characters is not
tracked, and so group mechanics come in to play.

*Hordes* on the other hand, are very large groups of people, where they have
not all been instantiated as Characters. The population of orcs hiding in the
mountains, for instance. Hordes can spawn groups. Hordes can have their
numbers decimated. It's simply impractical to store the data for each
individual in a horde. Rather, the Horde has dynamics of its own. Hordes can
represent armies. They can represent villages or towns or cities or even
entire nations. The race of celestial beings can be considered a horde as
well.

---------
Effect
---------

An *Effect* is a special object that doesn't really have a physical parallel.
It is an adjustment or change to something's properties. This change can come
from a spell or someone's ability or skill. It can also come from weilding a
simple weapon (it should increase your battle damage and effectiveness) or it
can come from a wound (your HP is reduced, and your ability is diminished). In
short, any change to an item or a character is an effect.

All Effects behave the same, as we'll see later.

Effects can be skills. Effects can be spells. They can be personality traits
or backgrounds or any number of things that may change the properties of an
Item, Character, or a Room. You may see me refer to things that are Effects by
the words "skill", "spell", etc... Keep in mind that they are really Effects.

------
Quest
------

Used to store quest states?

--------
Rule
--------

It may seem odd that *Rule* objects are an object in the Rule System, but
really, isn't that what a Rule System should have at its core?

A Rule is a special object that watches for a particular condition to occur.
When the condition occurs, it applies one or more Effect. A condition is simple a set
of attributes reaching a particular value on a set of objects. For instance,
"When someone enters the room, wait 5 seconds and then cast a Blinding Light
spell." Another rule is "when Blinding Light is cast, everyone in
the room received the effect temporary blindness for 1 minute."

Typically, Rules are bound to objects. In our example above, the Rule is
applied to an Area. Or perhaps it is tied to an Item in that Area.  The second
Rule is applied to an Effect, the spell Blinding Light.

----------------------
Clock
---------------------

The *Clock* object is rather simple. It keeps track of time. Each Area has a
time warp factor, so time will pass more slowly or more quickly in a
particular Area, but it is all keyed off of the singular Clock.

The possibility to have multiple clocks exist. However, I can't imagine a way
to handle times that pass in parallel. Perhaps the GM in a gaming session can
simply wind the clock back and forth as needed, and the toolkit will take care
of all the details.

--------------
Universe
---------------

The Universe is not an object, but rather, a concept. It is the collection of
all the objects in the universe, from Creatures to Areas and even the Clock.
In programming terms, it is the set of global variables. In philosophical
terms, it is everything.

---------------
Event Loop
---------------

At the center of everything is the Event Loop. The Event Loop maintains a
queue of events to process, sorted by the time when they are supposed to
occur. When the events are due, it executes them.

That sounds simple enough, of course. But what are Events? Events are special
objects that are created in a number of circumstances. It could be the
decision of a character to execute a certain action. It could be the damage
received from a strike. It could be a timer set to go off after a certain
time.

How are events executed? The answer is that they really aren't. The events
just fire when they are ready. As they fire, Rules pick up on them and process
their effects.

Since there is an Event Queue, the user of the Toolkit can actually step
through the events one at a time. The typical lifecucle of a series of events
is as follows.

* An action is declared by a character. This action is declared in a response
  to user input or perhaps due to some AI code that has been run. (AI code
  typically waits for events and processes them into actions.)

* Once the action is declared, that event is processed by the rules and
  effects. There is the possibility that some rule or action will forbid it.

* If the action is successfully declared, then effects are applied, sometimes
  after a certain time.


================
How Objects Interact
================

This section covers how objects interact with each other. This is a very
important topic, because it describes how YOU can change the rules of the game
or introduce your own.

---------------
Rules and the Event Queue
---------------

Rules and the Event Queue interact in a special, yet simple, way.

Each Rule has a *Filter*. This is a special object that, when given an event,
will determine whether the Rule should apply or not. The Filter specifies what
types of Events are being looked for, and perhaps which objects the Event has
a parameter for.

When the Event fires, each Rule's Filter is tested. (Now. there is a bit of
magic going along here. That's because applying 10,000 Rules to 10,000 events
involved 10,0000,000 checks. Because of the nature of the Filter, the Rules
can be organized to quickly find the Filters that do apply.) When a match is
found, the Event is passed to the Rule.

The Event has all the parameters that the Rule needs to implement its effects.

The interaction between Events and Rules are:

* The Rule may do some additional filtering. That is, even though the Rule is
  looking for a particular Event, it may not apply at a particular time.
* The Rule may apply some Effects to various objects.
* The Rule may queue up some additional Events as well.
* The Rule may ask for a decision by an actor. If this is a PC, then the PC
  will be asked for his input. If this is an NPC, then the GM will be asked
  for his input. The GM may have the creature wired up to an AI, which will
  offer its advice and the GM can either accept it or override it. Depending
  on the decision, Effects may be immediately applied, or Events queued for
  further application.

===========================
Details
===========================

Given the above, we can now define the details of the JGRPG Rule System.

-----------
All Objects
-----------

All Objects have the following attributes:

id (str)

  The unique identifier for each object. This is used in some places to refer
  exactly to another object. The id is likely a UUID in string format.

name (str)
  
  A name for the object. This need not be unique, but probably should be in
  most cases.

type (str)

  The type of the object. This is 'Character', 'Race', etc...

----
Race
----

The Race object stores all the attributes for a Race. It cannot have effects
applied to it. See :ref:`character generation` to see how Races are used to
create characters.

attribute_modifiers (dict of str:float)

  A table of attribute to modifier values. Each race can have an attribute
  modifier for each attribute. Missing attributes means the modifier is 0.

male_names (list of str)

  A list of random names for males of this race. Names that end with '-' are
  prefixes and names that end with '-' are suffixes. Random name generation
  may choose a random prefix and a random suffix to generate a name instead of
  one of the optional names.

female_names (list of str)

  A list of random female names for this race. Follows the same rules as
  male_names.

surnames (list of str)

  A list of random surnames for this race. Follows the same rules as
  male_names.

effects

  A list of Effects automatically applied to characters of this race.



.. _character generation:

--------------------
Character Generation
--------------------
