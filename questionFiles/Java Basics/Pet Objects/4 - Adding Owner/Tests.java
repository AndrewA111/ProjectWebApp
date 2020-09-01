import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class Tests {

	@TestDescription (value = "Check creating a dog assigns it the correct owner.")
	@TestHint (value = "Assign the passed 'owner' variable to 'this.owner'")
	@Test
	public void checkDogGetsOwner() {

		Owner owner = new Owner("Dave");
		Dog dog = new Dog("Buddy", owner);

		assertEquals("Creating a dog should assign it the owner passed in it's constructor.",
				owner,
				dog.getOwner());
	}

	@TestDescription (value = "Check creating a dog assigns it to the correct owner's pet list.")
	@TestHint (value = "Call the owner's addPet method to add a pet.")
	@Test
	public void checkOwnerGetsDog() {

		Owner owner = new Owner("Dave");
		Dog dog = new Dog("Buddy", owner);

		assertEquals("Creating a dog should assign it to its owner's pet list.",
				dog,
				dog.getOwner().getPetList().get(0));
	}

	@TestDescription (value = "Check creating a cat assigns it the correct owner.")
	@TestHint (value = "Assign the passed 'owner' variable to 'this.owner'")
	@Test
	public void checkCatGetsOwner() {

		Owner owner = new Owner("Dave");
		Cat cat = new Cat("Felix", owner);

		assertEquals("Creating a cat should assign it the owner passed in it's constructor.",
				owner,
				cat.getOwner());
	}

	@TestDescription (value = "Check creating a cat assigns it to the correct owner's pet list.")
	@TestHint (value = "Call the owner's addPet method to add a pet.")
	@Test
	public void checkOwnerGetsCat() {

		Owner owner = new Owner("Dave");
		Cat cat = new Cat("Buddy", owner);

		assertEquals("Creating a cat should assign it to its owner's pet list.",
				cat,
				cat.getOwner().getPetList().get(0));
	}
}