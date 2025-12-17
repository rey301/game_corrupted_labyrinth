from entities.item import Item

class Key(Item):
    """
    Defines keys for unlocking exits towards rooms in the game.
    """
    def __init__(self, name, description, weight, key_id):
        super().__init__(name, description, weight)
        self.key_id = key_id

    def use(self, player):
        """
        Unlock a directed exit according to the key's key_id and current room.
        :param player: The player that is in the game.
        :param room: The room that the player is currently in.
        :param world: The world that is in the game.
        :return: The string message after the door is unlocked or when the player is in the wrong room.
        """
        current_room = player.current_room
        # unlock data well
        if self.key_id == "4rch1ve":
            # player must be in the room to unlock
            if current_room.name == "glitch_pit":
                current_room.unlock_exit("east")
                return "The shard dissolves into the air. The Data Well gateway unlocks.", "remove"
            else:
                return "The data key hums faintly, but nothing happens here.", "keep"

        # one of two conditions for the final door to unlock
        if self.key_id == "decrypt":
            if current_room.name == "obsolete_hub":
                current_room.kernel_unlock = True
                return ("The console beeps, static starts to unwind revealing"
                        "\nthe door towards the System Kernel.", "remove")
            return "You need to be at the obsolete_hub to decrypt the final console.", "keep"

        # second condition for the final door to unlock
        # this key is only dropped by the gatekeeper
        if self.key_id == "k3rn3l":
            if current_room.name == "obsolete_hub" and current_room.kernel_unlock:
                current_room.unlock_exit("north")
                return ("The kernel key glows - heading towards door towards the System Kernel, "
                        "unlocking the final pathway."), "remove"
            return "The kernel key hums softly, but nothing happens here.", "keep"


        # used to unlock phantom node
        # this node exits straight to the gatekeeper node from data well and updates the description
        # to make it look like it appeared
        if self.key_id == "unlock_c0":
            if current_room.name == "boot_sector":
                current_room.unlock_exit("east")
                current_room.update_description(
                    """
| BOOT SECTOR |

System booting...
[ Initialising user shell ]
[ Loading visual layer    ]
[ Syncing input streams   ]

A plain-looking room forms around you, like the world is still loading.
 Bits of code fall from the ceiling. Something small glints on the floor.

Exits: NORTH -> Lost Cache, SOUTH -> Glitch Pit, EAST -> Phantom Node
                    """)
                return "A hidden doorway flickers open to the east...", "remove"
            return "The phantom key hums faintly, but nothing happens here.", "keep"
        return "The key hums faintly, but nothing happens here.", "keep"


