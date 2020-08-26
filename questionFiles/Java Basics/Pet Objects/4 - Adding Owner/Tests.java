import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class Tests {
	
	@TestDescription (value = "Check creating a dog assigns it the correct owner.")
	@Test
	public void checkDogGetsOwner() {

		Owner owner = new Owner("Dave");
		Dog dog = new Dog("Buddy", owner);
		
		assertEquals("Creating a dog should assign it the owner passed in it's constructor.", 
				dog.getOwner(),
				owner);
	}
	
	@TestDescription (value = "Check creating a dog assigns it to the correct owner's pet list.")
	@Test
	public void checkOwnerGetsDog() {

		Owner owner = new Owner("Dave");
		Dog dog = new Dog("Buddy", owner);
		
		assertEquals("Creating a dog should assign it to its owner's pet list.", 
				dog.getOwner().getPetList().get(0),
				dog);
	}
	
	@TestDescription (value = "Check creating a cat assigns it the correct owner.")
	@Test
	public void checkCatGetsOwner() {

		Owner owner = new Owner("Dave");
		Cat cat = new Cat("Felix", owner);
		
		assertEquals("Creating a cat should assign it the owner passed in it's constructor.", 
				cat.getOwner(),
				owner);
	}
	
	@TestDescription (value = "Check creating a cat assigns it to the correct owner's pet list.")
	@Test
	public void checkOwnerGetsCat() {

		Owner owner = new Owner("Dave");
		Cat cat = new Cat("Buddy", owner);
		
		assertEquals("Creating a cat should assign it to its owner's pet list.", 
				cat.getOwner().getPetList().get(0),
				cat);
	}
	

}
