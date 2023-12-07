#!/usr/local/bin/Rscript

# read lists of input times and distances
f <- file("stdin")
have_times <- FALSE
open(f)
while (length(line <- readLines(f, n = 1, warn = FALSE)) > 0) {
	values <- strsplit(gsub(".*:\\s+", "", line), split = " +") |> unlist()

  if (have_times) {
    distances <- values
  } else {
    times <- values
    have_times <- TRUE
  }
}

product <- 1

# let:
#   race time limit = t
#   current record distance = d
#   number of seconds you hold the button for = b
#
# then for the parabola b(t-b) - d,
# winning times to hold the button for are values
# of b where it's above the axis
for (i in 1:length(times)) {
  t <- as.numeric(times[i])
  d <- as.numeric(distances[i])
  
  # well-posed parabolas all are a vertical shift of a parabola that
  # (starts at the origin and has a vertex in the first quadrant)
  # so we know the left/right real roots of it
  left_root <- (t - sqrt(t*t - 4*d))/2
  right_root <- (t + sqrt(t*t - 4*d))/2
  
  # need to beat, not tie, the record so if the roots are integers
  # then they're not solutions
  # in both cases take the next integer over
  if (left_root == ceiling(left_root)) {
    left_int_root <- left_root + 1
  } else {
    left_int_root <- ceiling(left_root)
  }
  
  if (right_root == floor(right_root)) {
    right_int_root <- right_root - 1
  } else {
    right_int_root <- floor(right_root)
  }
  
  n_solutions <- right_int_root - left_int_root + 1
  
  print(left_root)
  print(right_root)
  print(n_solutions)
  product <- product * n_solutions
}

print(product)