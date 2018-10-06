package com.pchrzasz;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * @author Paweł Chrząszczewski
 */
class AggergationKata {


	public static void main(String[] args) {
		//Generate a basic array of students:
		        Student galina = new Student("Galina", 95, "Philology", Student.Gender.FEMALE);
		Student anton = new Student("Anton", 90, "CS", Student.Gender.MALE);
		Student jack = new Student("Jack", 82, "Philology", Student.Gender.MALE);
		Student mike = new Student("Mike", 60, "Philology", Student.Gender.MALE);
		Student jane = new Student("Jane", 65, "CS", Student.Gender.FEMALE);

		Student[] students = new Student[]{galina, anton, jack, mike, jane};

		Map<String, Double> averageGradeByDepartment = getAverageGradeByDepartment(Arrays.stream(students));

	}

	public static Map<String, Double> getAverageGradeByDepartment(Stream<Student> students) {
		return students.collect(Collectors.groupingBy(Student::getDepartment,
				Collectors.averagingDouble(Student::getGrade)));
	}

	public static Map<String, Long> getNumberOfStudentsByDepartment(Stream<Student> students) {
		return students.collect(Collectors.groupingBy(Student::getDepartment, Collectors.counting()));
	}

	public static Map<String, List<String>> getStudentNamesByDepartment(Stream<Student> students) {
		return students.collect(
				Collectors.groupingBy(
						Student::getDepartment,
						Collectors.mapping(Student::getName, Collectors.toList())
				)
		);
	}

	public static Map<String, Map<Student.Gender, Long>> getTheNumberOfStudentsByGenderForEachDepartment(Stream<Student> students) {
		return students.collect(
				Collectors.groupingBy(
						Student::getDepartment,
						Collectors.groupingBy(Student::getGender, Collectors.counting())
				)
		);
	}
}
