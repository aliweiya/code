<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ page session="false" %>
<html>
    <head>
        <title>Spittr</title>
        <link rel="stylesheet" type="text/css" href="<c:url value='/resources/style.css'/>" />
      </head>

      <body>
        <form method="POST">
            First Name: <input type="text" name="firstName" /><br/>
            Last Name: <input type="text" name="lastName" /><br/>
            Username: <input type="password" name="password" /><br/>
            <input type="submit" value="Register" />
        </form>
      </body>
</html>