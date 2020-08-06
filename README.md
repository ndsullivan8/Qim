# Qim NeoVim Python Plugin

## <a id="introduction"></a>Introduction

As part of the changes included in Neovim there is a new plugin model where
plugins are separate processes which Neovim communicates to using the
MessagePack protocol.

Since plugins are distinct from the Neovim process, it is possible to write
plugins in many languages.

This is a minimal example of a Python plugin. When you want to create a new
Python plugin, you should be able to (and feel free to) copy this repository,
rename a couple files, include the plugin in your Vim config and see something
happen.

## <a id="installing"></a>Installing

### <a id="install-neovim"></a>Install NeoVim
MAC-OS
`
homebrew install neovim
`

Devserver
`
sudo feature install neovim
`

Linux
`
$pkgmgr install neovim
`
### <a id="install-vim-plug"></a>Install vim-plug

(Note the of the vim-plug Directory!!!)
[vim-plug installation instructions](https://github.com/junegunn/vim-plug)

MAC-OS ( ~/.local/share/ <- Plug Directory)
`
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
`

### <a id="install-pynvim"></a>Install pynvim
Qim should be using Python3 by default 

`pip3 install pynvim` 

From neovim you can run `:CheckHealth` to verify python3 support

### Create a NeoVim init.vim file in ~/.config/nvim/init.vim 

This is your init.vim file (similar to .vimrc)
```
if &compatible
  set nocompatible               " Be iMproved
endif
" Plugins will be downloaded under the specified directory.
call plug#begin('~/.local/share/nvim/plugged')

" Qim
Plug 'ndsullivan8/Qim'

call plug#end()

syntax enable
```

Make sure you've added the Qim vim-plugin; add this line to the plugin section (see above):

```The Qim Plugin
Plug 'ndsullivan8/Qim'
```

### <a id="initializing"></a>Initializing Vim with Remote Plugin

The next thing to do is to initialize the manifest for the Python part of the
plugin. The manifest is a cache that Vim keeps of the interface implemented by
the Python part of the plugin. The functions and commands it implements.

To initialize the manifest, execute the following commands from neovim command line.

```NeoVim
:PluginInstall
```
Plugin install should install Qim

```NeoVim
:UpdateRemotePlugins
```
You should see the following rplugin file auto updated
`cat ~/.local/share/nvim/rplugin.vim`

The rplugin should contain something like this...
```
" python3 plugins
call remote#host#RegisterPlugin('python3', '/Users/nsully/.local/share/nvim/plugged/qim/rplugin/python3/qim.py', [
       \ {'sync': v:false, 'name': 'QimMain', 'type': 'function', 'opts': {}},
      \ ])
```


**NOTE:** After initializing the manifest, you must restart neovim for the python
functions be be available.

### <a id="testing"></a>Testing the New Plugin

There is some VimL in the plugin that will print when Neovim is starting up:

    Starting the example Python Plugin

That will confirm that the VimL portions of the plugin are loading correctly.

There is a function defined in the VimL portion of the plugin which echos some
text. You can execute the function like this:

```VimL
:exec HelloWorld()
```

Now that the manifest is initialized, it should be possible to invoke the
function defined in the Python part of the plugin. Look in \_\_init\_\_ to see
the implementation.

```VimL
:exec QimMain()
```

## <a id="development"></a>Development

On it's own, this plugin doesn't do anything interesting, so the expectation is
that you will want to modify it.

### <a id="debugging"></a>Debugging

In order to take advantage of the Python REPL and make it easier to test changes in your Python code, I usually take the following steps:

1. Open a Neovim instance.
2. Open a terminal inside Neovim. (:term)
3. Start the Python, or IPython, interpreter in the Neovim terminal. (python, ipython)
4. Execute this code in the Python interpreter:
```Python
import neovim
import os

nvim = neovim.attach('socket', path=os.environ['NVIM_LISTEN_ADDRESS'])
```

At this point, you can either execute commands directly against Neovim, to test the behavior of the interface:

```Python
nvim.current.buffer.name
```

or load your own plugin class and work with it directly.

```Python
%run "rplugin/python/nvim-example-python-plugin.py"
m = Main(nvim)
m.doItPython([])
```

### <a id="changing-interface"></a>Plugin Interface Changes

Neovim includes a step where the interface of the remote plugin is cached for
Neovim, so that Neovim knows what functions and commands your plugin is making
available without having to wait while the external process containing the
plugin is started.

```VimL
:UpdateRemotePlugins
```

Run this command for *every* change in the plugin interface. Without this, you
may see errors on from Neovim telling you methods are missing from your plugin.
Or the new functionality you are trying to add just won't work.

## <a id="troubleshooting"></a>Troubleshooting

### <a id="refreshing-manifest"></a>Refreshing the Manifest File

For each change to the interface of the Python plugin, that is to say, any
alterations to the @neovim decorators, you need to update Neovim's manifest
file:

```VimL
:UpdateRemotePlugins
```

Restart Neovim after you update to make the changes take effect.

If there is a syntax error in the Python file, it may result in the plugin not
loading. There may be no visible error. If you run the update command, and the
commands and functions defined in the remote plugin are not available, the next
useful troubleshooting step is to load your plugin directly in a Python
interpreter to see if it works.

### <a id="client-log-file"></a>Python Client Log File

Define this environment variable to get output logged from your Python client.

```Bash
export NVIM_PYTHON_LOG_FILE=${HOME}/.nvim-python.log
```

The output files will have a number appended, and should be visible with this:

```Bash
ls ${HOME}/.nvim-python.log*
```

### <a id="neovim-log-file"></a>Neovim Log File

```Bash
ls ~/.nvimlog
```

### <a id="neovim-library"></a>Neovim Library

One problem I encountered when I was first getting started was the Python
neovim module was not installed on my system. I didn't see any great errors
that lead me to that conclusion, so it is worth checking:

```Bash
python -c "import neovim"
```

Should execute without an error.

## <a id="references"></a>References
- [Neovim Remote Plugin Documentation](http://neovim.io/doc/user/remote_plugin.html)

The Neovim docs for remote plugins. It's a little sparse, but captures the core
detail.

- [Neovim Python Client](https://github.com/neovim/python-client)

The Neovim Python client is the Python API that wraps the MessagePack protocol
Neovim uses to communicate with remote plugins. If you are looking for more
information on how to use the vim parameter to the main object to control
Neovim, this is the place to go.
