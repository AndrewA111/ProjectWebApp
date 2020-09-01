/*
 * Class to represent a pet
 */
public class Pet {
	
	// pet name
	protected String name;
	
	/*
	 * Constructor (this is the 'super' constructor
	 * referenced in Dog and Cat when extending)
	 */
	public Pet(String name) {
		
		this.name = name;
	}
	
	// Method to describe a pet
	public String describe() {
		return "Name: " + name;
	}
	
	/*
	 * 'Getters' - these are used to access objects
	 *  of this class's private variables from code 
	 *  outside of this class
	 */	
	public String getName() {
		return name;
	}
}