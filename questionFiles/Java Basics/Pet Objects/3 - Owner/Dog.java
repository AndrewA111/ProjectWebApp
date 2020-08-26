/*
 * Class to represent a dog
 */
public class Dog extends Pet{
	
	// constructor
	public Dog(String name) {
		super(name);
	}
	
	// Make the dog bark
	public String bark() {
		return "Woof!";
	}
}
