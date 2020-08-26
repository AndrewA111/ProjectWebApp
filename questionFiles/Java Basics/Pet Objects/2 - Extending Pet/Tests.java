import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

public class Tests {
	
	@TestDescription (value = "Name should be assigned when Dog is constucted")
	@Test
	public void checkPetNameSet() {

		Dog dog = new Dog("Buddy");
		
		assertEquals("\'new Pet(\"Buddy\") should set name to \"Buddy\"", dog.getName(), "Buddy");
	}
	
	@TestDescription (value = "Dog should be a subclass of Pet")
	@Test
	public void checkDogExtendsPet() {

		Dog dog = new Dog("Buddy");
		
		assertTrue("Dog is not a subclass of Pet.", dog instanceof Pet);
	}
	
	@TestDescription (value = "'bark' method should return 'Woof!'")
	@Test
	public void checkBarkReturnsWoof() {

		Dog dog = new Dog("Buddy");
		
		assertEquals("Bark method does not return 'Woof!'", dog.bark(), "Woof!");
	}
}
