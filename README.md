# SaltStack extension for Visual Studio Code

This extension adds language colorization support for the SaltStack template language to VS Code.
The language is a yaml with Jinja2 templating.

![IDE](https://raw.githubusercontent.com/korekontrol/vscode-saltstack/master/example.png)

## Using the extension

First, you will need to install Visual Studio Code `1.19.0` or higher. In the command palette (`cmd-shift-p`) select `Install Extension` and choose `SaltStack`.

## Contributing

If you are interested in making this extension better, I will gladly take pull requests that expand it to add intellisense, hovers and validators. If you're not familiar with working on Visual Studio Code extensions, check out the VS Code extenders documentation at
https://code.visualstudio.com/docs.

To get started on the extension...

1. Go to the Debug viewlet and select `Launch Extension` then hit run (`F5`). This will launch a second instance of Code with the extension from the first window loaded.

2. As you make changes, you can also reload (`Ctrl+R` or `Cmd+R` on Mac) the second Code window to load any changes.

If you have a previous release of the extension installed and you perform these steps, Code will temporarily override the locally installed version instead for the one you're working on for the second window. The first (main) window will remain to have the locally installed, prior version installed and enabled until an update is available.

## Publishing

1. Bump version number in `package.json`

2. After git push, a build starts automatically. Publishing to marketplace requires manual approval in [Jenkins](https://jenkins.korekontrol.net/job/vscode-saltstack-publish/lastSuccessfulBuild/console)

## Credits
Created by [Marek Obuchowicz](https://github.com/marek-obuchowicz) from [KoreKontrol](https://www.korekontrol.eu/).

Many thanks to William Holroyd and Ross Neufeld.

## License
[MIT](LICENSE)
