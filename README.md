# SlurmTutorial

Diese Tutorial soll einen Einstieg in die Nutzung von Slurm geben.
Es wird angenommen, dass der Nutzer bereits mit der Nutzung von Linux vertraut ist.

## Was ist Slurm?

Slurm ist ein Job-Management-System, das es ermöglicht, Prozesse mittels sogenannten Jobs auf einem Cluster auszuführen.
Es ist in der Lage, die Ressourcen eines Clusters effizient zu verteilen und zu verwalten.
Slurm ist eine Open-Source-Software und kann unter 
[https://slurm.schedmd.com/](https://slurm.schedmd.com/) heruntergeladen werden.
In diesem Tutorial werden wir uns jedoch mit der Nutzung von Slurm befassen, nicht mit der Installation. 

## Wie funktioniert Slurm?

![slurm_bsp2](/img/slurm_bsp2.png)

Das vereinfachte Schema zeigt recht gut, wie Slurm funktioniert.
Slurm ist in der Lage, die Ressourcen eines HPCs effizient zu nutzen, in dem es die Jobs gleichmäßig auf die Nodes verteilt. 
Davon bekommt der User selber im bestenfalls gar nichts mit.
Allerdings kann es zum Beispiel bei dem Sharen von Ressourcen über zwei Nodes zu einer Verlangsamung des ausgeführten Codes kommen.
Manchmal ist es dann sinnvoll sicherzugehen, dass dies nicht geschieht, 
im Allgemeinen sollte man auf einem HPC damit jedoch keine Probleme haben,
da die Rechnungen meist nicht sonderlich zeitkritisch sind. 
Wichtig für den User ist jedoch die Spezifizierung seiner benötigten Hardwareressourcen. 
Dies ist die Hauptaufgabe im Umgang mit Slurm. 
Der Workload Manager benötigt vom User die Information, wie viele Ressourcen er über welche Laufzeit bereitstellen muss. 
Anhand dessen wird der User in eine Queue eingeordnet.
Benötigt ein User nun sehr viele Ressourcen und stehen diese aktuell nicht zur Verfügung muss der User warten,
bis seine Anwendung gestartet wird. 
Kleinere Jobs benötigen im Allgemeinen eine kürzere Wartezeit. 
Zu viele, zu kleine Jobs können einen HPC jedoch auch stark ausbremsen, da so nur selten Ressourcen für große Jobs zur Verfügung stehen. 
Um also eine optimale Nutzung des Clusters sicherzustellen, ist auch die Vorsicht und Rücksichtname der User gefragt.


## Wie kann ich Slurm nutzen?

Nun wissen wir wie Slurm prinzipiell funktioniert, doch wie interagieren wir nun mit dem Slurm deamons?
Für den User stellt Slurm dafür eine Reihe von Befehlen bereit, die es ermöglichen, Jobs zu erstellen, zu verwalten und zu beenden.
Diese Befehle sind in der Regel in der Form `s<command>` zu finden.
Die wichtigsten Befehle sind dabei:

- `sinfo`: Zeigt Informationen über die Cluster an
- `squeue`: Zeigt Informationen über alle Jobs an 
  - `squeue -u <username>`: Zeigt Informationen über die eigenen Jobs an
- `srun`: Startet einen Job 
- `sbatch`: Startet einen Job im Batch-Modus
- `scancel`: Beendet einen Job

## Wie kann ich Slurm nutzen, um Code auszuführen?

Wie bereits erwähnt, gibt es verschiedene Befehle, um Jobs zu starten.
Nun wollen wir darauf eingehen wie wir diese benutzen können um beispielsweise einen Python code auf dem Cluster ausführen können.
Zunächst wollen wir uns mit dem Befehl `srun` befassen, um einen Job zu starten. 
Der Befehl `srun` ist in der Form `srun <command>` zu verwenden und stellt die simpeleste Methode dar, um einen Job zu starten.
Zunächst muss der Nutzer angeben, wie viele Ressourcen er benötigt. An den Meisten HPCs sind bereits kleine Standards vorgegeben.
In diesem Tutorial wollen wir jedoch zeigen wie wir darüber hinaus Ressourcen verwalten können.
Dazu können wir verschiedenen Parameter verwenden. Die wichtigsten dabei sind:
- `-n, --ntasks` gibt an, wie viele tasks gleichzeittig im Job ausgeführt werden können.
- `-N` gibt an wie viele Nodes benötigt werden (nur nutzen sollte es unvermeidbar sein eine ganze Node zu verwenden) 
    - `--ntasks-per-node` gibt an, wie viele Tasks pro Node ausgeführt werden sollen.
- `-c` gibt an, wie viele CPUs (Kerne) pro Node benötigt werden.
- `--mem` gibt an, wie viel Arbeitsspeicher pro Node benötigt wird.
- `--time` gibt an, wie lange der Job maximal laufen darf.
- `--partition` gibt an, auf welchem Partition der Job ausgeführt werden soll.
- `--pty` gibt an, dass ein Pseudo-Terminal erzeugt werden soll, dadurch können Error Codes von Slurm ausgelesen werden, welche ansonsten durch den Absturz nicht ausgegeben werden würden.

Es gibt noch weitere Parameter, die in der Dokumentation von Slurm zu finden sind [https://slurm.schedmd.com/srun.html](https://slurm.schedmd.com/srun.html).

Ein Beispiel für einen Befehl, der einen Job startet, ist:

    srun -n 1 -c 1 --mem 1G --time 1:00:00 --partition=compute --export=ALL --pty python3 test.py

Dieser Befehl startet einen Job, welcher einen CPU Kern und 1GB Arbeitsspeicher zur verfügung hat.
Die Laufzeit beträgt eine Stunde, auf der Partition `compute` und wird im Pseudo-Terminal gestartet.
Das Pseudo-Terminal ist auch notwendig, damit der Nutzer mit dem Job interagieren kann.
Der Befehl `python3 test.py` ist der Befehl den `srun` auführen soll.

## Wie kann ich komplexere Jobs starten?

Komplexere Jobs können entweder durch das Ausführen einer `.sh` Datei durch `srun` gesehen, allerdings gibt es einen besseren Weg:
Slurm bietet die Möglichkeit, Jobs im sogenannten Batch-Modus durch den Befehl `sbatch` zu starten.
Nun wird der Code nicht mehr in einem aktiven Terminal ausgeführt.
Wir können jetzt nicht mehr live in den Terminal Output sehen, allerdings wird so ermöglicht, dass Jobs auch dann ausgeführt werden, 
wenn der User nicht mit dem Cluster direkt interagiert.
Daher sollte `sbatch` genutzt werden, wenn man größere Jobs abschickt und man nicht direkt einen Terminal Output benötigt. 
Dazu muss der Nutzer eine Datei erstellen, die den Befehl enthält, der ausgeführt werden soll.
Diese Datei muss mit der Endung `.sh` oder `.slurm` enden.
Innerhalb der Datei kann vollumfänglich auf Bash zugegriffen werden, wenn als Kopfzeile `#!/bin/bash` angegeben wird.
Hier können die Variablen jetzt durch den Prefix `#SBATCH` für den Job gesetzt werden. 
Dabei können die bereits von `srun` bekannten Commands verwendet werden.

 
Ein Beispiel für eine solche Datei ist `test.slurm`:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test.out           # Name of stdout output file
    #SBATCH --error=test.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G                    # RAM
    #SBATCH --partition=compute         # partition
    #SBATCH --ntasks-per-node=1         # tasks per Node  
    #SBATCH --cpus-per-task=1           # how much Cores per Task
    #SBATCH --export=ALL                # All of the user's environment will be loaded 
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    
    conda activate <conda_env>
    python3 test.py
    
Der Befehl:

    `sbatch test.slurm`

startet dann den Job.
Dabei fällt auf, dass nun zusätzliche Parameter gesetzt wurden. Dies geschieht, um den Workflow jetzt besser im Überblick zu haben.
Dazu gehören die Output Files `test.out`, sowie `test.err`. Dies sind Text Files, wobei `test.err` alle Errors listet welche während 
der Ausführung des Jobs aufgetreten sind und `test.out` den Terminal Output listet.
Zusätzlich bietet Slurm die Möglichkeit eine Mail zu senden, wenn ein Job startet, fehlschlägt oder erfolgreich beendet wurde. 
So wird der User über alle relevanten Vorkommnisse informiert, ohne selber auf dem Cluster eingeloggt sein zu müssen. 

## Wie kann ich gleichzeitig mehrere Jobs starten?

Slurm bietet die Möglichkeit, mittels sogenannten Job Arrays, mehrere Jobs gleichzeitig zu starten.
Dazu wird erneut eine Datei benötigt, die den Befehl enthält, der ausgeführt werden soll.
Ein Job Array wird mit dem Befehl `sbatch --array=1-10 test.slurm` gestartet.
Alternativ kann `#SBATCH --array=1-10` verwendet werden. 
Der Parameter `--array` gibt dabei an, wie viele Jobs gestartet werden sollen.
Innerhalb der Datei kann auf die Variable `$SLURM_ARRAY_TASK_ID` zugegriffen werden (hier 1-10).
Diese Variable gibt die ID des aktuellen Jobs an.
Ergänzten wir unsere output files mir einem `%A` und `%a` können wir die Job ID und die Array ID einfügen.
Dadurch kann der Befehl, der ausgeführt werden soll, angepasst werden.

Ein Beispiel für eine solche Datei ist `test.sh`:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test_%A_%a.out           # Name of stdout output file
    #SBATCH --error=test_%A_%a.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G                    # RAM
    #SBATCH --partition=compute         # partition
    #SBATCH --ntasks-per-node=1         # tasks per Node  
    #SBATCH --cpus-per-task=1           # how much Cores per Task
    #SBATCH --export=ALL                # All of the user's environment will be loaded 
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    #SBATCH --array=1-10                # array IDs
        
    conda activate <conda_env>
    python3 test.py $SLURM_ARRAY_TASK_ID

## Wie kann ich GPU Jobs starten?

Slurm bietet die Möglichkeit, GPU Jobs zu starten.
Genauso wie bei CPU Jobs muss der Nutzer die benötigten Ressourcen angeben.

Ein Beispiel für einen Befehl, der einen GPU Job startet, ist:

    srun -n 1 -c 1 --mem 1G --time 1:00:00 --partition=graphics --gpus-per-node=T4:1--export=ALL --pty bash python3 test.py

Nun wird anstelle von `--partition=compute` die Partition `--partition=graphic` verwendet. 
Diese ist mit GPUs ausgestattet.
Um die GPU zu nutzen, kann der Parameter `--gpus-per-node=[type:]number` verwendet werden. 
Dieser gibt die Anzahl und den Typen der GPUs an.
Im obigen Beispiel wird beispielsweise eine Nvidia T4 verwendet. 
Wie immer gibt es noch eine ganze Reihe weitere Parameter, welche verwendet werden können. 
Diese können erneut in der Dokumentation von `srun`, beziehungsweise `sbatch` nachgesehen werden.
Im folgenden noch ein Beispiel für eine `sbatch` kompatible Datei welche mehrere GPUs verwendet:

    #!/bin/bash
    #SBATCH --job-name=test              # Job name
    #SBATCH --output=test.out           # Name of stdout output file
    #SBATCH --error=test.err           # Name of stderr error file
    #SBATCH --time=0-1:00:00             # Time limit days-hrs:min:sec
    #SBATCH --mem=1G                    # RAM
    #SBATCH --partition=compute         # partition
    #SBATCH --ntasks-per-node=1         # tasks per Node  
    #SBATCH --cpus-per-task=1           # how much Cores per Task
    #SBATCH --export=ALL                # All of the user's environment will be loaded 
    #SBATCH --mail-type=START,END,FAIL   # notifications for job done & fail
    #SBATCH --mail-user=<email>          # email address
    
    #SBATCH --gpus=1               # total number of GPUs
    #SBATCH --gpus-per-node=1       # Anzahl der GPUs pro Node
    #SBATCH --gpus-per-task=1       # number of GPU per Task

    
    conda activate <conda_env>
    python3 test.py


## Nice to have:

Nun wissen wir, wie wir Jobs auf einem Cluster starten zu können.
Aber selbstverständlich gibt es noch immer kleine Dinge die uns das Leben erleichtern können. Einige sollen hier aufgelistet werden. 

### Starten eines interactiven Termninals auf einer Node:

Zum Testen oder Einrichten größerer Projekte kann es manchmal sinnvoll sein, statt auf der Login Node, auf einer „Working“ Node zu arbeiten. 
Daher hier ein Beispiel wie man ein Interactives Bash Terminal mit Slurm auf einer Node startet:  

    srun -c 6 --mem 8G --time 2:00:00 --partition=compute --export=ALL --pty bash

Wir starten also eine einfache Bash Umgebung auf einer Node. 
Sollten wir eine spezielle Node verwenden wollen, können wir `-w Nodename` verwenden, um Slurm darauf hinzuweisen,
welche Node verwendet werden soll. 

### Die Queue im Auge behalten:

Nehmen wir an, wir haben nun einige Jobs abgeschickt, die sich alle in der Queue befinden. 
Jetzt wollen wir regelmäßige Updates über den Status unseres Jobs, ohne immer wieder `squeue -u username` aufrufen zu müssen. 
Dafür können wir uns ein kleines Bash Skript erstellen, welches in einem Terminalfenster regelmäßig für uns die Queue updatet. <br>
Dazu müssen wir zunächst eine `.sh` Datei erstellen. Dafür können wir einfach den Terminal basierten Texteditor `nano` verwenden:

    nano queue.sh

Hier hinein kopieren wir nun einfach folgendes kleines Skript:

    username="username"
    squeue -u $username|grep PD|wc -l;
    squeue -u $username|grep '$username  R'|wc -l
    while :; do
            echo "Pending jobs: "
            squeue -u $username|grep PD|wc -l;
            echo "Running jobs: "
            squeue -u $username|grep '$username  R'|wc -l
            squeue -u $username;
            read -t 5;
    done;

Dabei ersetzen wir `"username"` in Zeile eins einfach durch den Namen unseres Linux Nutzers.
Anschließend können wir die Datei speichern (`Str+x`).
Nun können wir unsere Datei einfach über Bash starten und erhalten so regelmäßige Updates bezüglich unserer Queue: 
    
    bash queue.sh

Noch einfacher können wir es uns machen, wenn wir in unsere `.bashrc` einen kleinen Alias einfügen. 
Hier bitte Vorsicht, die `.bashrc` ist die Konfigurationsdatei unseres Terminals. Solltet wir hier etwas vollständig falsch machen, 
könnte unser Terminal danach vielleicht nicht mehr so funktionieren, 
wie wir uns das wünschen (mehr Informationen dazu hier: [https://wiki.ubuntuusers.de/Bash/bashrc/](https://wiki.ubuntuusers.de/Bash/bashrc/)). 

Die `.bashrc` liegt in unserem Home-Verzeichnis. Wir schreiben also:

    nano ~/.bashrc

Hier scrollen wir einfach bis ganz nach unten und fügen einen Alias hinzu:

    alias status='bash ~/queue.sh'

Dann speichern wir das ganz einfach wieder ab.
Nun müssen wir nur noch unsere `.bashrc` neu laden. Das können wir ganz einfach tun, in dem wir in Terminal:

    . ~/.bashrc

oder:

    source ~/.bashrc

schreiben.
Nun können wir in das Terminal einfach `status` schreiben und führen nun unser kleines Queue-Skript aus. 

<br>

Ich hoffe, ich konnte dir mit diesem Tutorial helfen. Nun wünsche ich dir viel Spaß beim Nutzen von Slurm.
