# SlurmTutorial

Diese Tutorial soll einen Einstieg in die Nutzung von Slurm geben.
Es wird angenommen, dass der Nutzer bereits mit der Nutzung von Linux vertraut ist.

## Was ist Slurm?

Slurm ist ein Job-Management-System, das es ermöglicht, ein mehrere Jobs auf einem Cluster auszuführen.
Es ist in der Lage, die Ressourcen eines Clusters effizient zu verteilen und zu verwalten.
Slurm ist Open Source und kann unter [https://slurm.schedmd.com/](https://slurm.schedmd.com/) heruntergeladen werden.

## Wie funktioniert Slurm?

![Slurm Architektur](img/slurm_bsp.png) 

![Slurm genauer](img/slurm_bsp2.png)

## Wie kann ich Slurm nutzen?

Für den User von Slurm gibt es eine Reihe von Befehlen, die es ermöglichen, Jobs zu erstellen, zu verwalten und zu beenden.
Diese Befehle sind in der Regel in der Form `s<command>` zu finden.
Die wichtigsten Befehle sind:

- `sinfo`: Zeigt Informationen über die Cluster an
- `squeue`: Zeigt Informationen über alle Jobs an 
  - `squeue -u <username>`:Zeigt Informationen über die eigenen Jobs an
- `srun`: Startet einen Job 
- `sbatch`: Startet einen Job im Batch-Modus
- `scancel`: Beendet einen Job

## Wie kann ich Slurm nutzen um Code auszuführen?

Wie bereits erwähnt, gibt es verschiedene Befehle, um Jobs zu starten.
In diesem Tutorial wird der Befehl `srun` verwendet, um einen Job zu starten. 
Der Befehl `srun` ist in der Form `srun <command>` zu verwenden.
Dazu muss der Nutzer angeben, wie viele Ressourcen er benötigt.
Dies geschieht mit verschiedenen Parametern:
- Der Parameter `-n` gibt an, wie viele Nodes benötigt werden.
- Der Parameter `-c` gibt an, wie viele CPUs pro Node benötigt werden.
- Der Parameter `--mem` gibt an, wie viel Arbeitsspeicher pro Node benötigt wird.
- Der Parameter `--time` gibt an, wie lange der Job maximal laufen darf.
- Der Parameter `--partition` gibt an, auf welchem Partition der Job ausgeführt werden soll.
- Der Parameter `--ntasks-per-node` gibt an, wie viele Tasks pro Node ausgeführt werden sollen.
- Der Parameter `--pty` gibt an, dass ein Pseudo-Terminal erzeugt werden soll.

Es gibt noch weitere Parameter, die in der Dokumentation von Slurm zu finden sind [https://slurm.schedmd.com/srun.html](https://slurm.schedmd.com/srun.html).

Ein Beispiel für einen Befehl, der einen Job startet, ist:

    srun -n 1 -c 1 --mem 1G --time 1:00:00 --partition=compute --export=ALL --pty bash python3 test.py

Dieser Befehl startet einen Job auf explizit einer Node, mit einem CPU Kern, 1GB Arbeitsspeicher, einer Laufzeit von 1 Stunde, auf der Partition `debug` und startet ein Pseudo-Terminal.
Das Pseudo-Terminal ist notwendig, damit der Nutzer mit dem Job interagieren kann.
Der Befehl `python3 test.py` ist der Befehl, der ausgeführt werden soll.

## Wie kann ich komplexere Jobs starten?

Slurm bietet die Möglichkeit, Jobs im Batch-Modus zu starten.
Dazu muss der Nutzer eine Datei erstellen, die den Befehl enthält, der ausgeführt werden soll.
Diese Datei muss mit der Endung `.sh` (vlt. noch andere) enden.
Innerhalb der Datei kann vollumfänglich auf Bash zugegriffen werden.
 
Ein Beispiel für eine solche Datei ist `test.sh`:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test.out           # Name of stdout output file
    #SBATCH --error=test.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G
    #SBATCH --partition=compute
    #SBATCH --ntasks-per-node=1
    #SBATCH --nodes=1
    #SBATCH --cpus-per-task=1
    #SBATCH --export=ALL
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    
    conda activate <conda_env>
    python3 test.py
    
Der Befehl `sbatch test.sh` startet dann den Job.

## Wie kann ich gleichzeitig mehrere Jobs starten?

Slurm bietet die Möglichkeit, mehrere Jobs gleichzeitig zu starten mittels job arrays.
Dazu wird erneut eine Datei benötigt, die den Befehl enthält, der ausgeführt werden soll.
Diese Datei muss mit der Endung `.sh` (vlt. noch andere) enden.
Ein Job Array wird mit dem Befehl `sbatch --array=1-10 test.sh` gestartet.
Der Parameter `--array` gibt dabei an, wie viele Jobs gestartet werden sollen.
Innerhalb der Datei kann auf die Variable `$SLURM_ARRAY_TASK_ID` zugegriffen werden.
Diese Variable gibt die ID des aktuellen Jobs an.
Dadurch kann der Befehl, der ausgeführt werden soll, angepasst werden.

Ein Beispiel für eine solche Datei ist `test.sh`:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test.out           # Name of stdout output file
    #SBATCH --error=test.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G
    #SBATCH --partition=compute
    #SBATCH --ntasks-per-node=1
    #SBATCH --nodes=1
    #SBATCH --cpus-per-task=1
    #SBATCH --export=ALL
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    #SBATCH --array=1-10
    
    conda activate <conda_env>
    python3 test.py $SLURM_ARRAY_TASK_ID

## Wie kann ich GPU Jobs starten?

Slurm bietet die Möglichkeit, GPU Jobs zu starten.
Genauso wie bei CPU Jobs, muss der Nutzer die benötigten Ressourcen angeben.

Ein Beispiel für einen Befehl, der einen GPU Job startet, ist:

    srun -n 1 -c 1 --mem 1G --time 1:00:00 --partition=graphics --gres=gpu:1 --export=ALL --pty bash python3 test.py

Nun wird anstellen von `--partition=compute` die Partition `graphics` diese ist mit GPUs ausgestattet.
Außerdem wird mit dem Parameter `--gres=gpu:1` angegeben, dass eine GPU benötigt wird.

Im folgenden noch ein Beispiel für eine `sbatch` kompatible Datei welche mehrere GPUs verwendet:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test.out           # Name of stdout output file
    #SBATCH --error=test.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G                    # Memory limit für die CPU
    #SBATCH --partition=graphics     # Partition mit GPUs
    #SBATCH --ntasks-per-node=1      # Anzahl der Tasks pro Node
    #SBATCH --cpus-per-task=1     # Anzahl der CPUs pro Task
    #SBATCH --gpus-per-node=5       # Anzahl der GPUs pro Node
    #SBATCH --export=ALL          # Exportiere alle Variablen
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    
    conda activate <conda_env>
    python3 test.py
