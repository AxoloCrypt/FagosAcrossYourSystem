# Fagos

Fagos Across Your System it’s an 8-bit shoot ‘em up game where you are a Fago in a microscopic world and the system you live it’s invaded by multiple bacteria and another weird thing. 
To survive you must shoot your DNA to these enemies to prevent the total infestation of the system, but be careful, the enemies are going to defend themselves!

![title](images-fagos/tittle.png)
![gameplay](https://user-images.githubusercontent.com/85807899/144197836-55c783aa-5382-468c-87d3-9dd35da445cf.gif)

## About
Created using [pyxel](https://github.com/kitao/pyxel) retro game engine under MIT license. 
This game was created for the Game Off 2021.  
We hope you like it!

## Controls

| Keys        | Commands               | Obs                                                           |
| ----------- | ---------------------- | ------------------------------------------------------------- |
| TAB         | PAUSE                  |                                                               |
| Q           | Quit                   | While the game it's in pause or instructed on the game.       |
| ENTER       | Resume the game        |                                                               |
| Arrow Keys  | Movement               |                                                               |
| Space       | Shoot                  |                                                               |
| Esc         | Close the game         |                                                               |

## Build

### Linux
```
docker build -t pyxel-build -f ./docker/linux-build-image .
docker create --name extract pyxel-build
docker cp extract:/tmp/fagos/dist/main ./fagos-linux-bin
docker rm extract
```

## Run Application (pyxel 1.5.0 or higher)
> Make sure you have pyxel retro game engine installed. 
#### Windows
```
pip install -U pyxel
```
#### Linux
```
sudo pip3 install -U pyxel
```
#### MacOs
```
pip3 install -U pyxel
```
After installing pyxel go to the current location of the .pyxapp file and use the following command:
```
pyxel play FagosAcrossYourSystem.pyxapp
```
## Contributing 
See the [Contributing Guideline](https://github.com/AxoloCrypt/FagosAcrossYourSystem/blob/master/CONTRIBUTING.md).
