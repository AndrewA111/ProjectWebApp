import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import org.junit.Test;

public class Tests {

	@TestDescription (value = "Dog's describe method should be overwritten to produce different output than Pet's describe class")
	@TestHint (value = "You should define a method 'describe()' in the Dog class.")
	@Test
	public void checkMethodOverWritten() {

		Dog dog = new Dog("Buddy");

		assertFalse("Describe method should be overwirrten in Dog class.",
				dog.describe().equals("Name: "+ dog.getName()));

	}

	@TestDescription (value = "Output of calling a Dog's describe() method should match spec.")
	@TestHint (value = "Have a look at the formatting in Cat.java")
	@Test
	public void checkDogExtendsPet() {

		Dog dog = new Dog("Buddy");

		assertEquals("Output format incorrect", "Name: " + dog.getName() + "\nAnimal: Dog", dog.describe());
	}
}
