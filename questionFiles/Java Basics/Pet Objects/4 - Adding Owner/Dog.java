/*
 * Class to represent a dog
 */
public class Dog extends Pet{
	
	// constructor
	public Dog(String name, Owner owner) {
		
		// constructor
		super(name, owner);
	}
	
	/*
	 * Method to describe a dog
	 */
	public String describe() {
		return "Name: " + this.name +
				"\nAnimal: Dog";
	}
}