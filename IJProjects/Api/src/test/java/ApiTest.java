import io.restassured.RestAssured;
import io.restassured.response.Response;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ApiTest {

    @Test
    public void testGoogleHomePageStatusCode() {
        // Ожидаемый результат
        int expectedStatusCode = 200;

        // Выполняем GET-запрос
        Response response = RestAssured
                .given()
                .baseUri("https://www.google.com")
                .when()
                .get();

        // Фактический результат
        int actualStatusCode = response.getStatusCode();

        // Выводим оба значения
        System.out.println("Expected status code: " + expectedStatusCode);
        System.out.println("Actual status code: " + actualStatusCode);

        // Сравниваем
        assertEquals(expectedStatusCode, actualStatusCode, "Статус-код не совпадает!");
    }
}
