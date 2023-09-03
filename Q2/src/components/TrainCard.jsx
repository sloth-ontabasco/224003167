import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

// eslint-disable-next-line react/prop-types
export default function TrainCard({trainNumber, trainName, departureTime, seatsAvailable, price, delayedBy}) {
    return (
        <Box sx={{ minWidth: 275 }}>
            <Card variant="outlined">
                <CardContent>
                    <Typography
                        sx={{ fontSize: 14 }}
                        color="text.secondary"
                        gutterBottom
                    >
                        Train Number: {trainNumber}
                    </Typography>
                    <Typography variant="h5" component="div">
                        Train Name: {trainName}
                    </Typography>
                    <Button>
                        <Typography variant="h6" component="div">
                            Departure Time: {departureTime} (Delayed by {delayedBy} minutes)
                        </Typography>
                    </Button>
                    <Typography variant="body2">
                        {seatsAvailable[0]} Sleeper Seats Available
                        <br />
                        {seatsAvailable[1]} AC Seats Available
                    </Typography>
                </CardContent>
                <CardActions>
                    <Button size="small">Book Sleeper: INR {price[0]}</Button>
                    <Button size="small">Book AC: INR {price[1]}</Button>
                </CardActions>
            </Card>
        </Box>
    );
}
