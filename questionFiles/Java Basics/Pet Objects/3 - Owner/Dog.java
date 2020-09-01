/*
 * Class to represent a dog
 */
public class Dog extends Pet{
	
	// constructor
	public Dog(String name) {
		super(name);
	}
	
	/*
	 * Method to describe a dog
	 */
	public String describe() {
		return "Name: " + this.name +
				"\nAnimal: Dog";
	}
}
