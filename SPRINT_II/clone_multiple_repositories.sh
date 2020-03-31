#!/bin/sh

getArray() {
    array=()
    while IFS= read -r line
    do
        array+=("$line")
    done < "$1"
}

mkdir -p ~/Git_Repos/labex2/repositories && cd ~/Git_Repos/labex2/repositories

getArray "/home/lucas.rotsen/Git_Repos/labex2/SPRINT_II/repository-list.txt"
for element in "${array[@]}"
do
  echo "Clonando $element ..."
  echo ""
  git clone $element

  echo "Calculando métricas ..."
  echo ""

  FOLDER=`ls`
  radon raw $FOLDER -jO /home/lucas.rotsen/Git_Repos/labex2/SPRINT_II/metrics/${FOLDER}.json

  echo "Removing all repos ..."
  rm -rf *

done

cd .. && rmdir repositories