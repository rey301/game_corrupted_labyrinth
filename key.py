from item import Item

class Key(Item):
    def __init__(self, name, description, weight, key_id):
        super().__init__(name, description, weight)
        self.key_id = key_id

    def use(self, player=None, room=None, world=None):
        # unlock data well
        if self.key_id == "4rch1ve":
            # player must be in the room to unlock
            if room.name == "glitch_pit":
                room.unlock_exit("east")
                return "The shard dissolves into the air. The Data Well gateway unlocks.", "remove"
            else:
                return "The data key hums faintly, but nothing happens here.", "keep"

        if self.key_id == "decrypt":
            if room.name == "obsolete_hub":
                room.kernel_unlock = True
                return ("The console beeps, static starts to unwind revealing"
                        "\nthe door towards the System Kernel.", "remove")
            return "You need to be at the obsolete_hub to decrypt the final console.", "keep"

        # this key is only dropped by the gatekeeper once defeated, unlocking final exit
        if self.key_id == "k3rn3l":
            if room.name == "obsolete_hub" and room.kernel_unlock:
                room.unlock_exit("north")
                return "The kernel key glows - heading towards door towards the System Kernel, unlocking the final pathway.", "remove"
            return "The kernel key hums softly, but nothing happens here.", "keep"

            # keys
            # used to unlock phantom node
            # this node exits straight to the gatekeeper node from data well
        if self.key_id == "unlock_c0":
            if room.name == "boot_sector":
                room.unlock_exit("east")
                room.update_description("""
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


