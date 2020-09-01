/*
 * Class to represent cat
 *
 * 'extends' means that Cat has all the
 * properties of the Pet class, and can
 * define its own properties in addition
 */
public class Cat extends Pet{

	// constructor
	public Cat(String name) {

		/*
		 * We need to call the constructor
		 * of the superclass (Pet), to make
		 * sure that the value 'name' is set
		 */
		super(name);
	}

	/*
	 * Method to describe a cat
	 */
	public String describe() {
		return "Name: " + this.name +
				"\nAnimal: Cat";
	}

}
