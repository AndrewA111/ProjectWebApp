import java.io.PrintStream;

/**
 * Class to represent workers
 * @author Andrew
 *
 */
public class Worker extends Person{
	
	// Boss
	private Boss boss;
	
	/*
	 * --- EDIT HERE ---
	 * 
	 * Update this constuctor as described in the method 
	 * comment below
	 * 
	 * ------------------
	 * 
	 * Constuctor
	 * 
	 * When creating a Worker object, user should pass their 
	 * name, DOB and boss
	 * 
	 * This should add the passed boss as this Worker's boss 
	 * and add this worker to the Boss's list of workers
	 */
	public Worker(String name, Date dob, Boss boss) {
		
		// Person constructor
		super(name, dob);
		
		// --- Insert here ---
		

	}
	
	/**
	 * 
	 * Assigns new boss. 
	 * Instructs current boss to remove this worker from their workers list.
	 * Instructs new boss to add this worker to their workers list
	 * @param b New boss
	 */
	public void new_boss(Boss b) {
		
		// Remove this worker from old boss's workers list
		this.boss.sub_worker(this);
		
		// Set boss
		this.boss = b;
		
		// Add this worker to boss's workers list
		this.boss.add_Worker(this);
	}
	
	/**
	 * Print method
	 * Displays name, dob and boss
	 */
	public void print(PrintStream ps) {
		super.print(ps);
		ps.print("Boss: " + this.boss.getName() + "\n");
	}
	
	/**
	 * Getter for boss
	 * @return boss
	 */
	public Boss get_boss() {
		return boss;
	}
	
	
}