# Copyright (c) 2023 Autodesk
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk.

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class MenuCustomization(HookBaseClass):
    """Hook to allow customizing the Flow Production Tracking menu in Alias."""

    def sorted_menu_commands(self, commands):
        """
        Return the given commands as a list in the order they should be displayed in the menu.

        The menu will display the commands in the order they are returned by this method. the
        default implementation will sort the commands alphabetically by command's app name,
        then the command name itself.

        The engine commands should be retrieved from the engine `commands` property. Apply
        any custom ordering to these commands.

        The commands are returned as a list of tuples, where the first item corresponds to the
        command dict entry key, and the second item is the command dict entry value.

        :param commands: The commands to add to the menu.
        :type commands: dict

        :return: The list of commands in order they should be displayed in.
        :rtype: List[tuple[str, dict]]
        """

        # To display menu commands in the order that they are defined in the config settings,
        # uncomment the line below. Note that this requirest Python >= 3.7 because it relies
        # on the dictionary preserve their order of insertion.
        # return list(commands.items())

        # Sort by the command app name (if not a context menu command), then the command name.
        return sorted(
            commands.items(),
            key=lambda command: (
                command[1]["properties"]["app"].display_name
                if command[1].get("properties", {}).get("app")
                and command[1].get("properties", {}).get("type", "default")
                != "context_menu"
                else "Other Items",
                command[0],
            ),
        )
