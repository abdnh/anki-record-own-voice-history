This Anki add-on enhances the ["Record Own Voice"](https://docs.ankiweb.net/studying.html#editing-and-more) option
in the reviewer by keeping all recorded audio files and providing a GUI to see previous recordings.

I wanted to record my pronunciation each time I see a word/sentence card and timestamp the recordings to track my progress.
I initially wrote a [simpler add-on](https://github.com/abdnh/anki-misc/blob/master/timestamp_recording/__init__.py)
that just prepends a timestamp before sound tags Anki generates after recording
in the editor window. But then I noticed this takes me a lot of time, as I have
to open the editor window each time, select the appropriate field, and click F5 to record.
I then remembered Anki's "Record Own Voice" option and thought of tweaking it to make my life easier.

I also tweaked the "Replay Own Voice" option to make it look for any previous
recordings associated with the current card.

The add-on doesn't modify the note contents in any way;
it saves the recordings in its folder and not in Anki's media folder.
Thus, recordings are not synced to AnkiWeb.

![The add-on's GUI](shot.png)

## AnkiWeb

You can download the add-on from its AnkiWeb page: https://ankiweb.net/shared/info/1508039970

## Credit

Icons are taken from [Bootstrap Icons](https://icons.getbootstrap.com/) and licensed under the MIT license.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Support & feature requests

Please post any questions, bug reports, or feature requests in the [support page](https://forums.ankiweb.net/c/add-ons/11) or the [issue tracker](https://github.com/abdnh/anki-record-own-voice-history/issues).

If you want priority support for your feature/help request, I'm available for hire.
Get in touch via [email](mailto:abdo@abdnh.net) or the UpWork link below.

## Support me

Consider supporting me if you like my work:

<a href="https://github.com/sponsors/abdnh"><img height='36' src="https://i.imgur.com/dAgtzcC.png"></a>
<a href="https://www.patreon.com/abdnh"><img height='36' src="https://i.imgur.com/mZBGpZ1.png"></a>
<a href="https://www.buymeacoffee.com/abdnh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="36" ></a>

I'm also available for freelance add-on development:

<a href="https://www.upwork.com/freelancers/~01d764ac58a0eccc5c"><img height='36' src="https://i.imgur.com/z9lPvHb.png"></a>
