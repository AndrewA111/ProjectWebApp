/*
 * Class to represent a dog
 * 
 * Take a look at the implementation for
 * the 'Cat' class.
 * 
 * In a similar way, update this Dog class
 * to overwrite the 'describe' method given in
 * the Pet class
 */

/*
 * Note that Dog extends (inherits) Pet
 */
public class Dog extends Pet{

	// constructor
	public Dog(String name) {

		/*
		 * We need to call the constructor
		 * of the superclass (Pet), to make
		 * sure that the value 'name' is set
		 */
		super(name);
	}

	/*
	 * Overwrite the describe method to return:
	 *
	 * 	'Name: <name>
	 * 	Animal: Dog'
	 *
	 * where name is the name of this dog
	 */

}
