$(document).ready(function() {
            function fetchTasks() {
                $.ajax({
                    url: "http://localhost:8000/tasks/",
                    method: "GET",
                    success: function(tasks) {
                        let tableBody = "";
                        tasks.forEach(task => {
                            tableBody += `<tr>
                                            <td>${task.id}</td>
                                            <td>${task.title}</td>
                                            <td>${task.description || "-"}</td>
                                            <td>${task.completed ? "Yes" : "No"}</td>
                                         </tr>`;
                        });
                        $("#taskTableBody").html(tableBody);
                    },
                    error: function(error) {
                        console.error("Fehler:", error);
                    }
                });
            }

            fetchTasks();
        });