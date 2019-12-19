<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ page session="false" %>
<html>
    <head>
        <title>Spittr</title>
        <link rel="stylesheet" type="text/css" href="<c:url value='/resources/style.css'/>" />
      </head>

      <body>
        <c:forEach items="${spittleList}" var="spittle">
            <li id="spittle_<c:out value='spittle.id'/>">
                <div class="spittleMessage">
                    <c:out value="${spittle.message}" />
                </div>

                <div>
                    <span class="spittleTime"><c:out value='${spittle.name}' /></span>
                </div>
            </li>
        </c:foreach>
      </body>
</html>