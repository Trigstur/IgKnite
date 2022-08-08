'''
Predefined embeds to use across scripts.
---

MIT License

Copyright (c) 2022 HitBlast

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


# Imports.
import random
import disnake


# A really simple function to generate random footers!
def generate_footer() -> str:
    samples = [
        'When pigs fly...',
        'Stunned stork!',
        'A perfect debugged life doesn\'t exist.'
    ]
    return random.choice(samples)


# Override disnake.Embed class to form custom embeds.
class ClassicEmbed(disnake.Embed):
    '''
    Represents an embed common to all the normal commands.
    '''

    def __init__(self, inter: disnake.ApplicationCommandInteraction) -> None:
        super().__init__(
            color=3158326
        )

        self.set_footer(
            text=generate_footer(),
            icon_url=inter.author.avatar
        )


class ErrorEmbed(ClassicEmbed):
    '''
    Represents an embed common to all error messages.
    '''

    def __init__(self, inter: disnake.ApplicationCommandInteraction) -> None:
        super().__init__(
            color=16608388
        )

        self.set_footer(
            text=generate_footer(),
            icon_url=inter.author.avatar
        )