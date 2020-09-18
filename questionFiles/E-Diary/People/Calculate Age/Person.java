/*
 * Class to represent person
 */
public class Person {

	/*
	 * Names
	 */
	private String firstName;

	private String surname;

	/*
	 * Date of birth
	 */
	private Date dob;


	/*
	 *  Constructor
	 */
	public Person(String fname, String sname, Date dob) {
		this.firstName = fname;
		this.surname = sname;
		this.dob = dob;
	}

	/*
	 * Implement the 'age' method to return a person's
	 * age on a given date d
	 *
	 * You can assume d is a date after the person's
	 * date of birth (dob)
	 */

    public int age(Date d) {
		return -1;
	}

	/*
	 * Getters
	 */

	public String getFirstName() {
		return firstName;
	}


	public String getSurname() {
		return surname;
	}

	public Date getDob() {
		return dob;
	}
}
