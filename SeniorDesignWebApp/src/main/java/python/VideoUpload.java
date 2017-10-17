package python;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.file.Paths;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

@SuppressWarnings("serial")
public class VideoUpload extends HttpServlet {

	public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {

		// PythonInterpreter interpreter = new PythonInterpreter();
		// interpreter.exec("import sys\nsys.path.append('pathToModiles if
		// they're not there by default')\nimport video");
		// // execute a function that takes a string and returns a string
		// PyObject someFunc = interpreter.get("funcName");
		// PyObject result = someFunc.__call__(new PyString("Test!"));
		// String realResult = (String) result.__tojava__(String.class);
		Process p = null;
		File currentDir = new File(".tmp");
		String t = this.getClass().getPackage().getName() + ".";
		try {
			p = Runtime.getRuntime().exec("python \\src\\main\\java\\python\\video.py");
			p.waitFor();
			BufferedReader read = new BufferedReader(new InputStreamReader(p.getErrorStream()));
			String s = null;
			while ((s = read.readLine()) != null) {
				System.out.println(s);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		response.sendRedirect("video.jsp?file=terrain_w1anmt8er__PM.mp4");
	}
}