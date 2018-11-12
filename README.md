# Culinary

## What is Culinary?

Culinary is a Python program I have quickly writtent to dispatch build jobs onto various virtual machines (and possibly directly on the host machine). It was designed to run those build jobs in *sequence* to avoid overloading my computer. It is best used with a separate low-powered computers that can go through the builds sequentially while your main computer stays available for actually working.

## How to use it?

You simply have to run **Compile.py**. It takes two arguments. The first one is the project name. A corresponding json file must be available in the current directory. An example of such a file is given in **Example.json**. A branch must be given as a second parameter. For instance, to run with the master branch for the example project, you would run:

```
$ ./Compile.py Example master
```

By default all configurations defined in the json file are executed. If additional arguments are provided, then only the corresponding configurations are run.

