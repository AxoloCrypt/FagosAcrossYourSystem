# Fagos

Fagos Across Your System it’s an 8-bit shoot ‘em up game where you are a Fago in a microscopic world and the system you live it’s invaded by multiple bacteria and another weird thing. 
To survive you must shoot your DNA to these enemies to prevent the total infestation of the system, but be careful, the enemies are going to defend themselves!

![title](images-fagos/tittle.png)
![gameplay](https://user-images.githubusercontent.com/85807899/144197836-55c783aa-5382-468c-87d3-9dd35da445cf.gif)

## About
Created using [pyxel](https://github.com/kitao/pyxel) retro game engine under MIT license. 

This game was created for the Game Off 2021.
We hope you like it!

## Credits
- Juan Carlos Cardona (Username: JuCa) Programming and Sound
- Renata Ochoa (Username: Renosaurio) Graphics and Mapping

## Build

### Linux
```
docker build -t pyxel-build .
docker create --name extract pyxel-build
docker cp extract:/tmp/fagos/dist/main ./fagos
docker rm extract
```
