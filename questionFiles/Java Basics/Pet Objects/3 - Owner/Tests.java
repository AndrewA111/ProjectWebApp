import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import org.junit.Test;

public class Tests {

	@TestDescription (value = "Check petList is not null")
	@TestHint (value = "Use 'new ArrayList<Pet>()' to create a new ArrayList")
	@Test
	public void checkListNotNull() {

		Owner owner = new Owner("Dave");

		assertNotNull("petList instance variable must be initialized on creation of an owner object",
				owner.getPetList());
	}

	@TestDescription (value = "Dog should be able to be added to Owner's petList")
	@TestHint (value = "use the .add() method of ArrayList, passing the method the desired pet 'p'")
	@Test
	public void checkCanAddDog() {

		Owner owner = new Owner("Dave");
		Dog dog = new Dog("Buddy");

		owner.addPet(dog);

		assertEquals("'addPet(Dog d)' should add a dog to Owner's petList", dog, owner.getPetList().get(0));
	}

	@TestDescription (value = "Cat should be able to be added to Owner's petList")
	@TestHint (value = "use the .add() method of ArrayList, passing the method the desired pet 'p'")
	@Test
	public void checkCanAddCat() {

		Owner owner = new Owner("Dave");
		Cat cat = new Cat("Felix");

		owner.addPet(cat);

		assertEquals("'addPet(Cat c)' should add a cat to Owner's petList", cat, owner.getPetList().get(0));
	}
}