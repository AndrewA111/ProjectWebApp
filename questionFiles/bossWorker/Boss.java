import java.io.PrintStream;
import java.util.ArrayList;

/**
 * Class to represent bosses
 * @author Andrew
 *
 */
public class Boss extends Person {
	
	// List of workers
	private ArrayList<Person> workers;
	
	// Current position in list of workers
	private int currentWorker;
	
	public Boss(String name, Date dob) {
		// Person constructor
		super(name, dob);
		
		// Create list of Person objects
		this.workers = new ArrayList<Person>();
	}
	
	/**
	 * Method to add worker to workers
	 * @param w Worker to be added to workers
	 */
	protected void add_Worker(Worker w) {
		workers.add(w);
	}
	
	/**
	 * Method to remove worker from workers
	 * @param w worker to be removed from workers
	 */
	protected void sub_worker(Worker w) {
		workers.remove(w);
	}
	
	/**
	 * Method to return next person in list
	 * @return next person in list, or null if list empty
	 */
	public Worker next() {
		
		// if list empty, return null
		if(this.workers.size() < 1) {
			return null;
		}
		
		// check index not out of range
		if(!(this.currentWorker < this.workers.size())) {
			this.reset();
		}
		
		// store current worker
		Worker w = (Worker) this.workers.get(this.currentWorker);
		
		// increment currentWorker
		this.currentWorker++;
		
		// return stored worker
		return w;
	}		
	
	/**
	 * Sets list position to 0
	 */
	public void reset() {
		this.currentWorker = 0;
	}
	
	/**
	 * Print method
	 * Displays name, dob and number of workers
	 */
	public void print(PrintStream ps) {
		super.print(ps);
		
		// Temp variable to store current position in workers
		int temp = this.currentWorker;
		
		// Check workers list not empty
		if(this.workers.size() < 1) {
			ps.print("No workers.");
			return;
		}
		
		// reset position to start of list
		this.reset();
		
		ps.print("Workers:\n");
		
		// Loop through list
		while(currentWorker < this.workers.size()) {
			ps.print(this.workers.get(currentWorker).getName() + "\n");
			this.next();
		}
		
		// reset currentWorker to original value
		this.currentWorker = temp;
		
	}
	
	/**
	 * Getter for workers list
	 * @return
	 */
	public ArrayList<Person> getWorkers() {
		return workers;
	}
}
