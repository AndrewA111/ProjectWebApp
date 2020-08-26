import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class Tests {
	
	@TestDescription (value = "Name should be assigned when Pet is constucted")
	@Test
	public void checkPetNameSet() {

		Pet pet = new Pet("Buddy");
		
		assertEquals("\'new Pet(\"Buddy\") should set name to \"Buddy\"", pet.getName(), "Buddy");
	}
}
