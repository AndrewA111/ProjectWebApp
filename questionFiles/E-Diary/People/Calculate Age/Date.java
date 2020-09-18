/*
 * Class to represent a date
 */
public class Date {

	private int day;

	private int month;

	private int year;

	// Constructor
	public Date(int d, int m, int y) {
		this.day = d;
		this.month = m;
		this.year = y;
	}

	/*
	 * toString method
	 *
	 * Returns a String representation of a Date object
	 * and is used when an object is treated as a string
	 * (e.g. printed)
	 */
	public String toString() {
		return String.format("%02d/%02d/%4d",
							this.day, this.month, this.year);
	}

	/*
	 * Getters
	 */
	public int getDay() {
		return day;
	}

	public int getMonth() {
		return month;
	}

	public int getYear() {
		return year;
	}
}
