import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class Tests {
	@TestDescription (value = "Age should be correct when selected date falls before dob in calendar")
	@TestHint (value = "If given date before dob in calendar, age is (given_year - year_of_birth - 1)")
	@Test
	public void checkAgeBeforeBirthday() {

		Person person  = new Person("Dave", "Smith", new Date(10,6,1980));

		assertEquals("Person born on 10/6/1980 should be 19 on 21/1/2000",
				19, person.age(new Date(21,1,2000)));
	}

	@TestDescription (value = "Age should be correct when selected date falls after dob in calendar")
	@TestHint (value = "If given date after dob in calendar, age is (given_year - year_of_birth)")
	@Test
	public void checkAgeAfterBirthday() {

		Person person  = new Person("Dave", "Smith", new Date(9,5,1990));

		assertEquals("Person born on 9/5/1990 should be 25 on 1/7/2015",
					25, person.age(new Date(1,7,2015)));
	}

	@TestDescription (value = "Person should be 0 on their date of birth.")
	@TestHint (value = "Look out for 'off-by-one' errors.")
	@Test
	public void checkZeroOnDob() {

		Person person  = new Person("Dave", "Smith", new Date(9,5,1980));

		assertEquals("Person should be zero on the day they were born",
					0, person.age(new Date(9,5,1980)));
	}
}
