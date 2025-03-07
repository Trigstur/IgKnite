'''
The `Inspection` cog for IgKnite.
---

MIT License

Copyright (c) 2022 IgKnite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import math
# Imports.
from datetime import datetime
from time import mktime

import disnake
from disnake import Option, OptionType, Invite
from disnake.ext import commands

import core
from core.datacls import LockRoles


# The actual cog.
class Inspection(commands.Cog):
    def __init__(
            self,
            bot: core.IgKnite
    ) -> None:
        self.bot = bot

    # guildinfo
    @commands.slash_command(
        name='guildinfo',
        description='Shows all important information about the server.',
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _guildinfo(
        self,
        inter: disnake.CommandInteraction
    ) -> None:
        embed = core.TypicalEmbed(inter).add_field(
            name='Birth',
            value=datetime.strptime(
                str(inter.guild.created_at), '%Y-%m-%d %H:%M:%S.%f%z'
            ).strftime('%b %d, %Y')
        ).add_field(
            name='Owner',
            value=inter.guild.owner.mention
        ).add_field(
            name='Members',
            value=inter.guild.member_count
        ).add_field(
            name='Roles',
            value=len(inter.guild.roles)
        ).add_field(
            name='Channels',
            value=len(inter.guild.text_channels) + len(inter.guild.voice_channels)
        ).add_field(
            name='Identifier',
            value=inter.guild_id
        )

        if inter.guild.icon:
            embed.set_thumbnail(url=inter.guild.icon)

        await inter.send(embed=embed)

    # Backend for userinfo-labelled commands.
    # Do not use it within other commands unless really necessary.
    async def _userinfo_backend(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member = None
    ) -> None:
        member = inter.author if not member else member

        embed = core.TypicalEmbed(inter).set_title(
            value=str(member)
        ).add_field(
            name='Status',
            value=member.status
        ).add_field(
            name='Birth',
            value=datetime.strptime(
                str(member.created_at), '%Y-%m-%d %H:%M:%S.%f%z'
            ).strftime('%b %d, %Y')
        ).add_field(
            name='On Mobile',
            value=member.is_on_mobile()
        ).add_field(
            name='Race',
            value="Bot" if member.bot else "Human"
        ).add_field(
            name='Roles',
            value=len(member.roles)
        ).add_field(
            name='Position',
            value=member.top_role.mention
        ).add_field(
            name='Identifier',
            value=member.id
        ).set_thumbnail(
            url=member.display_avatar
        )
        await inter.send(embed=embed)

    # userinfo (slash)
    @commands.slash_command(
        name='userinfo',
        description='Shows all important information on a user.',
        options=[
            Option(
                'member',
                'Mention the server member.',
                OptionType.user
            )
        ],
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _userinfo(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member = None
    ) -> None:
        await self._userinfo_backend(inter, member)

    # userinfo (user)
    @commands.user_command(
        name='Show User Information',
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _userinfo_user(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member
    ) -> None:
        await self._userinfo_backend(inter, member)

    # roleinfo
    @commands.slash_command(
        name='roleinfo',
        description='Shows all important information related to a specific role.',
        options=[
            Option(
                'role',
                'Mention the role.',
                OptionType.role,
                required=True
            )
        ],
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _roleinfo(
        self,
        inter: disnake.CommandInteraction,
        role: disnake.Role
    ) -> None:
        embed = core.TypicalEmbed(inter).set_title(
            value=f'Role information: @{role.name}'
        ).add_field(
            name='Birth',
            value=datetime.strptime(
                str(role.created_at), '%Y-%m-%d %H:%M:%S.%f%z'
            ).strftime('%b %d, %Y')
        ).add_field(
            name='Mentionable',
            value=role.mentionable
        ).add_field(
            name='Managed By Integration',
            value=role.managed
        ).add_field(
            name='Managed By Bot',
            value=role.is_bot_managed()
        ).add_field(
            name='Role Position',
            value=role.position
        ).add_field(
            name='Identifier',
            value=f'`{role.id}`'
        )

        await inter.send(embed=embed)

    # invites

    @commands.slash_command(
        name='invites',
        description='Displays active server invites',
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _invites(
            self,
            inter: disnake.CommandInteraction,
    ) -> None:
        # Get the list of invites for this server and save this locally
        self.invites = await inter.guild.invites()
        self.page = page = 1

        invites_per_page = 5
        top_page = math.ceil(len(self.invites) / invites_per_page)

        async def load_page(page_num):

            self.page = page_num
            embed = core.TypicalEmbed(inter)  # initiates embed object
            embed.set_title("Invites")
            embed.set_description("List of all invites within the server")
            embed.set_footer(text=f"{self.page}/{top_page}")

            for invite in range((page_num * invites_per_page) - invites_per_page, page_num * invites_per_page):
                if invite < len(self.invites):
                    if self.invites[invite].max_age == 0:
                        max_age = 'never'
                    else:
                        # turn time struct into datetime object
                        date_time = datetime.fromtimestamp(mktime(self.invites[invite].expires_at.timetuple()))
                        # get UNIX timestamp for use in discord time display
                        max_age = f"<t:{int(mktime(date_time.timetuple()))}:R>"

                    embed.add_field(
                        name=f"#{invite + 1} [``{self.invites[invite].code}``]",
                        value=f"🧍{self.invites[invite].inviter.name}"
                              f" **|** 🚪 {self.invites[invite].uses}"
                              f" **|** 🕑 {max_age} \n\n",
                        inline=False
                    )
            return embed

        thisEmbed = await load_page(page)
        await inter.send(
            embed=thisEmbed,
            view=InviteMenu(
                inter,
                load_page,
                top_page,
                page,
                await inter.guild.invites()
            )
        )

    # audit
    @commands.slash_command(
        name='audit',
        description='Views the latest entries of the audit log in detail.',
        options=[
            Option(
                'limit',
                'The limit for showing entries. Must be within 1 and 100.',
                OptionType.integer
            )
        ],
        dm_permission=False
    )
    @commands.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _audit(
        self,
        inter: disnake.CommandInteraction,
        limit: int = 5
    ):
        if limit not in range(1, 101):
            await inter.response.send_message(f'{limit} is not within the given range.', ephemeral=True)

        else:
            embed = core.TypicalEmbed(inter).set_title(
                value=f'Audit Log ({limit} entries)'
            )
            async for audit_entry in inter.guild.audit_logs(limit=limit):
                embed.add_field(
                    name=f'- {audit_entry.action}',
                    value=f'User: {audit_entry.user} | Target: {audit_entry.target}',
                    inline=False
                )

            await inter.send(embed=embed, ephemeral=True)


# Invitation menu class
class InviteMenu(disnake.ui.View):
    def __init__(
            self,
            inter: disnake.CommandInteraction,
            page_loader,
            top_page: int = 1,
            page: int = 1,
            invites: list[Invite] = []
    ):
        super().__init__()
        self.page_loader = page_loader
        self.page = page
        self.top_page = top_page
        self.invite_list = []
        self.add_item(InviteDropdown(inter, invites))

        if self.page + 1 > self.top_page:
            self.children[1].disabled = True

    @disnake.ui.button(
        emoji="◀️",
        style=disnake.ButtonStyle.blurple,
        disabled=True,
    )
    async def go_down(
            self,
            button: disnake.ui.Button,
            inter: disnake.MessageInteraction
    ):
        self.page -= 1

        # If the page is at the bottom
        # Disable the down button it
        if self.page == 1:
            self.children[0].disabled = True
        else:
            # otherwise (re)enable it
            self.children[0].disabled = False
        # if the page has met the top page (the highest possible)
        # Disable the up button
        if self.page + 1 > self.top_page:
            self.children[1].disabled = True
        else:
            # otherwise (re)enable it
            self.children[1].disabled = False

        thisEmbed = await self.page_loader(self.page)
        await inter.response.edit_message(
            embed=thisEmbed,
            view=self,
        )

    @disnake.ui.button(
        emoji="▶️",
        style=disnake.ButtonStyle.blurple
    )
    async def go_up(
            self,
            button: disnake.ui.Button,
            inter: disnake.MessageInteraction
    ):
        self.page += 1

        # If the page is at the bottom
        # Disable the down button it
        if self.page == 1:
            self.children[0].disabled = True
        else:
            # otherwise (re)enable it
            self.children[0].disabled = False
        # if the page has met the top page (the highest possible)
        # Disable the up button
        if self.page + 1 > self.top_page:
            self.children[1].disabled = True
        else:
            # otherwise (re)enable it
            self.children[1].disabled = False

        thisEmbed = await self.page_loader(self.page)
        await inter.response.edit_message(
            embed=thisEmbed,
            view=self,
        )


# Invitation dropdown class
class InviteDropdown(disnake.ui.Select):

    def __init__(
            self,
            inter: disnake.CommandInteraction,
            invites: list[Invite] = []
    ):
        self.inter = inter
        # until 25 | discord only allows a max of 25 items to be displayed on the select option
        # and thus we will limit invites being processed to 25
        self.invites = invites[0:25]
        options = []
        for i in range(len(self.invites)):
            options.append(
                disnake.SelectOption(
                    label="#{} - {}".format(i + 1, invites[i].code),
                    value=i,
                    description=invites[i].inviter.name
                )
            )

        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        index = int(self.values[0])
        invite = self.invites[index]

        if invite.max_age == 0:
            max_age = 'never'
        else:
            # turn time struct into datetime object
            date_time = datetime.fromtimestamp(mktime(invite.expires_at.timetuple()))
            # get UNIX timestamp for use in discord time display
            max_age = f"<t:{int(mktime(date_time.timetuple()))}:R>"

        if invite.max_uses == 0:
            usage = f'{invite.uses} / ∞'
        else:
            usage = f'{invite.uses} / {invite.max_uses}'

        embed = core.TypicalEmbed(inter)  # initiates embed object
        embed.set_title("Invite | `{}`".format(invite.code))
        embed.set_description("Detailed overview of invite information")
        embed.add_field(
            name="Inviter",
            value=invite.inviter
        )
        embed.add_field(
            name="Code",
            value=invite.code
        )
        embed.add_field(
            name="Link",
            value="https://discord.gg/{}".format(invite.code)
        )
        embed.add_field(
            name="Expires",
            value=max_age
        )
        embed.add_field(
            name="Usage",
            value=usage
        )

        await inter.response.send_message(
            embed=embed,
            ephemeral=True
        )


# The setup() function for the cog.
def setup(bot: core.IgKnite) -> None:
    bot.add_cog(Inspection(bot))
