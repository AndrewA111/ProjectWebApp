import java.io.PrintStream;

public class Person {
	private String name;
	private Date dob;
	
	public Person(String n, Date d) {
		this.name = n;
		this.dob = d;
	}
	
	/*
	 * Method to print out person's name and DOB
	 */
	public void print(PrintStream ps) {
		ps.print("Name: " + this.name + "\tDOB: ");
		this.dob.print(ps);
	}

	public String getName() {
		return name;
	}
	
	/*
	 * Method to check Person's ages on a given date 'today'
	 * Returns age if 'today' is before 'dob'
	 * Returns -1 if dob is after 'today'
	 */
	public int getAge(Date today) {

		int age;
		
		// check if before birthday for given year
		if(today.getMonth() < this.dob.getMonth()
			|| (today.getMonth() == this.dob.getMonth() && 
				today.getDay() < this.dob.getDay()))
		{
			age = today.getYear() - this.dob.getYear() -1;
		}
		// otherwise, on or after birthday for given year
		else 
		{
			age = today.getYear() - this.dob.getYear();
		}
		
		if (age >= 0) {
			return age;
		}
		// if age < 0, input is considered invalid, return -1
		else {
			return -1;
		}
		
	}


}