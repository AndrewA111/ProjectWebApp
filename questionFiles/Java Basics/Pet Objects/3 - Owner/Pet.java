public class Pet {
	
	// pet name
	private String name;
	
	/*
	 * Complete the constructor to assigned the passed
	 * argument to the instance variable name
	 */
	public Pet(String name) {
		
		this.name = name;
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
