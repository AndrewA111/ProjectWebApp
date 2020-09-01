public class Pet {
	
	// pet name
	protected String name;

	// variable to track owner
	private Owner owner;

	/*
	 * Constructor
	 *
	 * Note, new argument 'owner' added. This must
	 * also be included in the Cat and Dog classes'
	 * constructors (this has been completed for you).
	 */
	public Pet(String name, Owner owner) {

		this.name = name;

		/*
		 * Assign owner to this pet's 'owner' instance variable
		 */


		/*
		 * Then add this pet to the owner
		 */

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

	public Owner getOwner() {
		return owner;
	}
}
