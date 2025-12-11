from item import Item

class Misc(Item):
    def __init__(self, name, description, weight, misc_id):
        super().__init__(name, description, weight)
        self.misc_id = misc_id

    def use(self, player=None, room=None, world=None):
        """
        When certain items are used, it causes something to happen in the world, or to the player (e.g.
        reading logs).
        :param player: The player that is currently in the game.
        :param room: The room that the player is currently in.
        :param world: The world with attributes of the game.
        :return: The text that will be printed to the user, and the flag if the item gets removed.
        """
        # for expanding backpack
        if self.misc_id == "bag_upgrade":
            prev_max = player.max_weight
            player.max_weight += 5
            return f"Your storage expands. \n{prev_max}+5 --> {player.max_weight}", "remove"

        # once activated in the data well, the lore items can be read
        if self.misc_id == "log":
            if room.name == "Data Well":
                player.scannable = True
                return "You activate the log module: hidden log fragments become readable.", "remove"
            return "You try to activate the log module. It beeps in error.", "keep"

        # keys
        # used to unlock phantom node
        # this node exits straight to the gatekeeper node from data well
        if self.misc_id == "unlock_c0":
            if room.name == "boot_sector":
                room.unlock_exit("east")
                room.update_description("""
+----------------------------- BOOT SECTOR ------------------------------+
    System booting...

        [ Initialising user shell ]
        [ Loading visual layer    ]
        [ Syncing input streams   ]

    A plain-looking room forms around you, 
    like the world is still loading.
    Bits of code fall from the ceiling. 
    Something small glints on the floor.

    Exits: NORTH -> Lost Cache, SOUTH -> Glitch Pit, EAST -> Phantom Node
+------------------------------------------------------------------------+
                """)
                return "A hidden doorway flickers open to the east...", "remove"
            return "The key hums faintly, but nothing happens here.", "keep"

        # unlock data well
        if self.misc_id == "d4t4":
            # player must be in the room to unlock
            if room.name == "glitch_pit":
                room.unlock_exit("east")
                return "The shard dissolves into the air. The Data Well gateway unlocks.", "remove"
            else:
                return "The data key hums faintly, but nothing happens here.", "keep"

        # this key is only dropped by the gatekeeper once defeated, unlocking final exit
        if self.misc_id == "kernel":
            if room.name == "Obsolete Hub":
                if "north" in room.exits:
                    return "The kernel pathway is already unlocked."
                room.set_exit("north", world.rooms["d2"])
                return "The kernel key glows - heading towards door towards the system kernel, unlocking the final pathway.", "remove"
            return "The kernel key hums softly, but nothing happens here.", "keep"

        # lore items
        if player.scannable:
            if self.misc_id == "lore1":
                return """
Memory Fragment Recovered: The Fall of the System

Users once navigated freely here.
This labyrinth was never meant to imprison —
it was a learning environment,
a controlled simulation for exploring unstable data structures.

Then something changed.
The system kernel fractured,
and the world began rewriting itself without supervision.
                """, "keep"
            if self.misc_id == "lore2":
                return """
Memory Fragment Recovered: The First Corruption

Corruption log: Severity Red.

An unknown signal entered the simulation.
A user connection was forcibly hijacked.
Subsystems responded by sealing pathways and
creating defensive entities to contain the breach.

The system was trying to protect you…
or protect itself from you.
                """, "keep"
            # this lore is retrievable after defeating the gatekeeper
            if self.misc_id == "lore3":
                return """
Memory Fragment Recovered: Origin of the Gatekeeper

Architect Note:
If the kernel is ever compromised,
an autonomous guardian will be instantiated.

It will not understand trust.
It will not negotiate.

It will defend the kernel until the system resets…
or until it is destroyed.
                """, "keep"
            if self.misc_id == "lore4":
                return """
Memory Fragment Recovered: The Truth
The labyrinth was not corrupted by accident.
Someone rewrote the rules.
Someone wanted you trapped.

And the Gatekeeper…
was created from your own user profile.

It was built to keep you from remembering why.
                """, "keep"
        else:
            return "You need to activate the scan module to read the logs.", "keep"

        return None




