/*
 * Class to represent a dog
 */
public class Dog extends Pet{
	
	// constructor
	public Dog(String name, Owner owner) {
		
		// constructor
		super(name, owner);
	}
	
	// Make the dog bark
	public String bark() {
		return "Woof!";
	}
}
