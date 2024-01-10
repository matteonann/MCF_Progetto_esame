# MCF_Progetto_esame
La presente repository contiene i due programmi costituenti il progetto da me svolto per l'esame di Metodi Computazionali per la Fisica, a.a. 2023-2023.

Il primo script, wpack.py, è una libreria creata per generare, osservare e studiare pacchetti d'onda. In particolare, vi è definita la classe w_packet, i cui oggetti sono dei pacchetti d'onda caratterizzati da determinate frequenze, corrispondenti ampiezze e da una particolare relazione di dispersione. 
Gli attributi e i metodi della classe sono descritti nella libreria con delle docstring, ma, per completezza, vengono riportati anche qui sotto:

Attributi:

- freqs : array/list
        Frequenze contenute nel pacchetto.
  
- amplitudes : array/list
        Ampiezze associate alle frequenze.
  
- disp : list
        Il primo elemento è la funzione che restituisce il k dalla relazione di dispersione, i successivi sono gli eventuali parametri della funzione

Metodi (oltre al costruttore):

- display_components_df(**kwargs) :
        Mostra un dataframe di "Pandas" con l'elenco delle frequenze, e relative ampiezze, contenute nel pacchetto	
	
- generate_wave_x(x, t, **kwargs) :
        Calcola la forma d'onda del pacchetto lungo l'asse x all'istante t tramite la formula

	
  	wf = sum_i (A_i*cos(k_i*x-2*pi*f_i*t)), con
 
	-i = indice che scorre tutti gli elementi dell'array delle frequenze (e ampiezze)
  
	-f_i = i-esima frequenza
  
	-A_i = i-esima ampiezza
  
	-k_i = i-esimo numero d'onda (restituito dalla relazione di dispersione)
  
	-x = array delle posizioni in cui campionare il pacchetto d'onda
  
	-t = istante fissato al quale calcolare la forma d'onda

 
- generate_wave_t(t, x, **kwargs) :
        Calcola la forma d'onda del pacchetto lungo l'asse t alla posizione x tramite la stessa formula indicata precedentemente, con la differenza che in questo caso t è un array e x è un float
	
- wave(axis, **kwargs) :
	Chiama uno dei due metodi "generate_" descritti sopra (in base al valore di axis passato) e rappresenta graficamente la forma d'onda.  

- animate(d, step, xx, **kwargs) :
        Chiama il metodo wave per rappresentare la forma d'onda lungo l'asse x (nei punti dell'array "xx") ad ogni istante che va da 0 a "d" con passo "step". I plot sono uniti in un'animazione di "matplotlib" che può essere salvata dall'utente.

- power_spectrum(t, x) :
        Chiama il metodo "generate_wave_t" per generare dapprima la forma d'onda lungo l'asse t all'intervallo di tempo e nella posizione specificati. Successivamente, calcola la trasformata di Fourier e le frequenze con i metodi ".rfft" e ".rfftfreq" di "scipy.fft", per poi calcolare le potenze (moduli quadri dei coefficienti di Fourier). Se specificato, esegue anche il plot dello spettro di potenza.


Il secondo script, wpack_test.py, è un programma in cui viene testata la libreria wpack creando un pacchetto d'onda e chiamando i metodi definiti per la classe w_packet.

Per prima cosa vengono definite delle distribuzioni di probabilità con cui generare le frequenze e le ampiezze da assegnare al pacchetto, così come delle funzioni che restituiscono i k (numeri d'onda) dati dalle frequenze generate secondo diverse relazioni di dispersione. Successivamente, dopo aver importato la libreria, attraverso un "argparse" si scelgono le distribuzioni e la relazione da usare per la creazione del pacchetto. La scelta delle opzioni è descritta di seguito (si può visualizzare la descrizione dell'argparse anche eseguendo il comando python3 wpack_test.py --help o python3 wpack_test.py -h).

usage: wpack_test.py [-h] [-fd FREQ_DIST] [-ad AMPL_DIST] [-dr DISP_REL]

Choosing freq/ampl distributions and dispersion relations

options:

  -h, --help            show this help message and exit
  
  -fd FREQ_DIST, --freq_dist FREQ_DIST
  
                        Frequency distribution. Choose from the following:
                        1) p(f) = f/3 for f in [0, 2], 2/3(3-f) for f in (2, 3] (default)
                        2) p(f) = 2/9 f for f in [0, 3]
			
  -ad AMPL_DIST, --ampl_dist AMPL_DIST
  
                        Amplityde distribution. Choose from the following:
                        1) p_f(A) = A for A in [0, a*sqrt(f)] (default)
                        2) p_f(A) = (1+f)^3 A^2 for A in [0, 1/(1+f)]
			
  -dr DISP_REL, --disp_rel DISP_REL
  
                        Dispersion relation. Choose from the following:
                        1) w = sqrt(ck)
                        2) w = sqrt(ck^2) (default)
                        3) w = sqrt(ck^3)
                        4) w = sqrt(b+ck^2)

Generate le frequenze e le ampiezze, viene chiesto all'utente se vuole visualizzare

- l'istogramma normalizzato delle frequenze generate (insieme al plot della distribuzione di robabilità)
- l'istogramma delle ampiezze generate
- l'istogramma delle frequenze generate, pesate secondo le ampiezze (con l'opzione "weights" di "matplotlib.pyplot.hist")

Con le frequenze e le ampiezze generate e la relazione di dispersione scelta, si crea l'oggetto "packet", di cui viene immediatamente visualizzata la forma d'onda rispetto all'asse x (con il metodo "wave") nei punti dell'array "x_0". In seguito vengono chiamati i seguenti metodi, chiedendo per ciascuno il permesso all'utente:

- display_components_df, chiedendo di specificare se vuole stampare la tabella in ordine crescente di frequenze o decrescente di ampiezze
- animate, per generare l'animazione dei primi 20 secondi (con passo 0.1 s) dell'evoluzione temporale del pacchetto, rappresentandola nell'intervallo campionato di posizioni "x_evo". Viene anche chiesto all'utente se vuole salvare l'animazione.
- power_spectrum, in due posizioni diverse (x=0 e x=x_f), per calcolare la trasformata di Fourier e rappresentare gli spettri di potenza (partendo dalla forma d'onda tracciata in corrispondenza dei punti dell'array "t"). Nella posizione x=0 viene anche tracciato lo spettro della parte reale (2*abs(fft)/len(t)) per confrontarlo con l'istogramma delle frequenze del pacchetto pesate con le ampiezze. Infine, dopo aver ampliato l'array "t", si ricalcolano le trasformate di Fourier nelle posizioni 0 e "x_f" e si confrontano i due spettri di potenza, osservandone l'uguaglianza.


Nel programma "wpack_test.py" i parametri delle distribuzioni e delle relazioni di dispersione sono stati fissati dal sottoscritto ai seguenti valori:
- dist A 1: a = 1;
- disp 1: c = 9e16
- disp 2: c = 9e16
- disp 3: c = 9e16
- disp 4: b = -1000, c = 9e16

Allo stesso modo, si sono ricercati e impostati anche dei valori ottimali delle altre variabili che vengono utilizzate nel programma (gli array di posizioni e tempi a cui vengono visualizzati i plot o calcolate le trasformate di Fourier, la durata e lo step dell'animazione...) per garantire una corretta visualizzazione dei pacchetti. L'utente può comunque intervenire nel programma  modificando i valori di tutti i parametri, cambiando di conseguenza, se necessario, anche gli intervalli spaziali e temporali in cui vengono visualizzati i pacchetti, in modo da assicurarsi che la parte rilevante del pacchetto non venga tagliata fuori dalla finestra di visualizzazione.
