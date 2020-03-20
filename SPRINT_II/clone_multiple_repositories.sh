#!/bin/sh

readarray array -t a < /home/lucas.rotsen/Git_Repos/labex2/SPRINT_II/repository-list.txt

mkdir -p ~/Git_Repos/labex2/repositories && cd ~/Git_Repos/labex2/repositories

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