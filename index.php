<?php require_once "config.php"; ?>
<!doctype html>
<html lang="tr">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

    <title>SAN ODEV</title>

    <style>
        body {
            background-color: #f2f2f2;
        }

    </style>
</head>
<body>

<div class="container">
    <div class="row">
        <div class="col-lg-6 offset-3">
            <div class="card my-5">
                <div class="card-body">

                    <form method="post" action="predict.php">
                        <div  class="form-group">
                            <label>
                                Hotel Name
                                <?php
                                $sql = $db->prepare("SELECT DISTINCT hotelname FROM sandata ORDER BY hotelname ASC");
                                $sql->execute();
                                $hotelNames = $sql->fetchAll(PDO::FETCH_ASSOC);
                                ?>
                                <select class="form-control" name="hotelname">
                                    <?php foreach ($hotelNames as $hotelName) : ?>
                                        <option value="<?= $hotelName['hotelname'] ?>"><?= $hotelName['hotelname'] ?></option>
                                    <?php endforeach; ?>
                                </select>
                            </label>
                        </div>
                        <div  class="form-group">
                            <label>
                                Departure Date
                                <input type="date" class="form-control" name="departureDate">
                            </label>
                        </div>
                        <div  class="form-group">
                            <label>
                                Return Date
                                <input type="date" class="form-control" name="returnDate">
                            </label>
                        </div>
                        <input type="submit" class="btn btn-outline-dark" value="Fiyat AL">
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
</body>
</html>
